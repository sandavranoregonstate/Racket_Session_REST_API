from datetime import date

from rest_framework.parsers import JSONParser
from .models import TheUser , Schedule, Location , Match , Result , Feedback
from .serializers import ResultSerializer ,  MatchSerializer , FeedbackSerializer

from django.db.models import Q
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response

class ListSchedule(APIView):
    parser_classes = (JSONParser,)

    def get(self, request):
        # Extracting the id_user from the request URL query
        id_user = request.GET.get('id_user')

        # From the database get the list of all “Schedule” entry
        schedules = Schedule.objects.filter(id_user=id_user)

        # Prepare the response data, making sure to return the name of the location, not the id
        data_r = {
            'items': [
                {
                    'id_schedule': schedule.id_schedule,
                    'location': schedule.location.name,  # Return the name of the location
                    'date': schedule.date,
                    'type': schedule.type,
                    'start_time': schedule.start_time
                }
                for schedule in schedules
            ]
        }

        data_n = data_r[ "items"]

        data_n.sort(key=lambda match: (match[ "date"], match[ "start_time"]))

        # Return a list of “Schedule” entry to the client
        return Response(data_n, status=status.HTTP_200_OK)

    def post(self, request):

        print( request.data )

        # Extracting the data from the request body
        id_user = request.data['id_user']
        location_string = request.data['location']
        date = request.data['date']
        type = request.data['type']
        start_time = request.data['start_time']

        # Make sure to convert location, which is a string to the id_location, in order to add it as a foreign key
        try:
            location = Location.objects.get(name=location_string)
        except Location.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        schedules = Schedule.objects.get( id_user= TheUser.objects.get( id_user = id_user ), location=location, date=date, type=type, start_time=start_time)

        if len( schedules ) == 0 :
            # Create the “Schedule” entry using the data from the input, except the drill list
            schedule = Schedule(id_user= TheUser.objects.get( id_user = id_user ), location=location, date=date, type=type, start_time=start_time)
            schedule.save()

        pair(schedule)

        return Response(status=status.HTTP_201_CREATED)


def create_the_match_entry( the_input , schedule ) :
    this_match = Match.objects.create( id_player_a = the_input.id_user , id_player_b = schedule.id_user , location = the_input.location , the_current_status_a = "pending" , the_current_status_b = "pending" , date = the_input.date , type = the_input.type , start_time = the_input.start_time )
    this_match.save()

    print( this_match)

# the_input = Schedule entry
def pair( the_input : Schedule ) :

    date = the_input.date
    start_time = the_input.start_time
    type = the_input.type
    location = the_input.location
    id_schedule = the_input.id_schedule

    # get all of the Schedule entry with the matching set of the criteria

    list_schedule = Schedule.objects.filter( date = date , start_time = start_time , type = type , location = location )
    list_schedule = [ x for x in list_schedule if x.id_schedule != id_schedule ]

    # create a Match entry for this schedule and every schedule

    for schedule in list_schedule :
        create_the_match_entry(the_input , schedule)

class ViewSchedule(APIView):

    parser_classes = (JSONParser,)

    def get(self, request, id_schedule):
        # Get the schedule entry with the same id_schedule as id_schedule from the URL
        try:
            schedule = Schedule.objects.get(id_schedule=id_schedule)
        except Schedule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Prepare the response data
        response_data = {
            'Schedule': {
                'id_schedule': id_schedule,
                'location': schedule.location.name,
                'date': schedule.date,
                'type': schedule.type,
                'start_time': 10
            },
        }

        # Return the “Schedule” entry and list of “Drill” entry
        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request, id_schedule):
        try:
            schedule = Schedule.objects.get(id_schedule=id_schedule)
        except Schedule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class MatchList(APIView):

    def get(self, request):

        id_user = request.GET.get('id_user')

        type_current = request.GET.get('type')
        training_or_competitive = request.GET.get('toc')
        usatt_rating = int( request.GET.get('ur'))
        is_expired = request.GET.get('ie')

        # two of the users have accepted the match, it is a session
        if type_current == "is_session":
            matches = Match.objects.filter(Q(the_current_status_a='accepted', the_current_status_b='accepted') |
                                           Q(the_current_status_a='accepted', the_current_status_b='accepted'))

        # the current player has neither accepted nor rejected the match
        elif type_current == "pending":
            matches = Match.objects.filter(Q(id_player_a=id_user, the_current_status_a='pending') |
                                           Q(id_player_b=id_user, the_current_status_b='pending'))

        # the current player has accepted the match
        elif type_current == "accepted":
            matches = Match.objects.filter(
                Q(id_player_a=id_user, the_current_status_a='accepted', the_current_status_b='rejected') |
                Q(id_player_a=id_user, the_current_status_a='accepted', the_current_status_b='pending') |

                Q(id_player_b=id_user, the_current_status_b='accepted', the_current_status_a='rejected') |
                Q(id_player_b=id_user, the_current_status_b='accepted', the_current_status_a='pending')

            )

        # the current player has rejected the match
        elif type_current == "rejected":
            matches = Match.objects.filter(Q(id_player_a=id_user, the_current_status_a='rejected') |
                                           Q(id_player_b=id_user, the_current_status_b='rejected'))

        else:
            # Handle the case where type_current doesn't match any known type
            matches = []


        # filter for is_expired

        current_date = date.today()

        print( len( matches ))

        if is_expired == "future" :
            matches = [match for match in matches if match.date > current_date]
        else :
            matches = [match for match in matches if match.date <= current_date]
        print(len(matches))

        # filter for usatt rating


        print( len( matches ))

        new_matches = []
        for x in matches :

            if x.id_player_a.id_user == id_user :
                if (usatt_rating - 250) < x.id_player_b.real_world_rating < usatt_rating :
                    new_matches.append( x )

            else :
                if (usatt_rating - 250) < x.id_player_a.real_world_rating < usatt_rating :
                    new_matches.append( x )

        matches = new_matches

        print( len( matches ))



        # filter for training or competitive


        print( len( matches ))


        if training_or_competitive == "competitive" :
            matches = [match for match in matches if match.type == "competitive"]
        else :
            matches = [match for match in matches if match.type == "training"]

        print( len( matches ))

        matches.sort(key=lambda match: (match.date, match.start_time))



        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)


class ViewMatch(APIView):

    def get(self, request, id_match):
        # Get the Match entry
        try:
            match = Match.objects.get(id_match=id_match)
        except Match.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MatchSerializer(match )

        # Return the “Schedule” entry and list of “Drill” entry
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListPendingFeedback(APIView):

    def get(self, request):
        id_user = request.GET.get('id_user')
        if id_user is None:
            return Response({'error': 'id_user is required'}, status=status.HTTP_400_BAD_REQUEST)

        feedbacks = Feedback.objects.filter( id_player_a = id_user , status='pending')

        serializer = FeedbackSerializer(feedbacks, many=True)

        return Response(serializer.data)


class ViewPendingFeedback(APIView):

    def get(self, request, id_pending_feedback):
        # Get the Feedback entry
        try:
            feedback = Feedback.objects.get(id_feedback=id_pending_feedback, status='pending')
        except Feedback.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data)

    def patch(self, request, id_pending_feedback):
        # Get the Feedback entry
        try:
            feedback = Feedback.objects.get(id_feedback=id_pending_feedback, status='pending')
        except Feedback.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Update the fields with the input from the request body
        feedback.serve_feedback = request.data.get('serve_feedback')
        feedback.receive_feedback = request.data.get('receive_feedback')
        feedback.forehand_loop_feedback = request.data.get('forehand_loop_feedback')
        feedback.backhand_loop_feedback = request.data.get('backhand_loop_feedback')
        feedback.forehand_block_feedback = request.data.get('forehand_block_feedback')
        feedback.backhand_block_feedback = request.data.get('backhand_block_feedback')
        feedback.personal_feedback = request.data.get('personal_feedback')
        feedback.status = 'completed'
        feedback.save()

        # Call the CalculateTheSkillPoint method (not implemented here)
        # CalculateTheSkillPoint()

        return Response(status=status.HTTP_204_NO_CONTENT)



class ListCompletedFeedback(APIView):

    def get(self, request):
        id_user = request.GET.get('id_user')
        if id_user is None:
            return Response({'error': 'id_user is required'}, status=status.HTTP_400_BAD_REQUEST)

        feedbacks = Feedback.objects.filter(id_player_a = id_user , status='completed')

        serializer = FeedbackSerializer(feedbacks, many=True)

        return Response(serializer.data)


class ViewCompletedFeedback(APIView):

    def get(self, request, id_completed_feedback):
        # Get the Feedback entry
        try:
            feedback = Feedback.objects.get(id_feedback=id_completed_feedback, status='completed')
        except Feedback.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data)

    def post(self, request, id_completed_feedback):
        # Get the Feedback entry
        try:
            feedback = Feedback.objects.get(id_feedback=id_completed_feedback, status='completed')
        except Feedback.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Set the status to "pending"
        feedback.status = 'pending'
        feedback.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ListPendingResults(APIView):

    def get(self, request):
        id_user = request.GET.get('id_user')
        if id_user is None:
            return Response({'error': 'id_user is required'}, status=status.HTTP_400_BAD_REQUEST)

        results = Result.objects.filter(
            status='pending',
            id_match__in=Match.objects.filter(Q(id_player_a__id_user=id_user) | Q(id_player_b__id_user=id_user))
        )

        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)

class ViewPendingResult(APIView):

    def get(self, request, id_pending_result):
        # Get the Result entry
        try:
            result = Result.objects.get(id_result=id_pending_result, status='pending')
        except Result.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ResultSerializer(result)
        return Response(serializer.data)

    def patch(self, request, id_pending_result):
        # Get the Result entry
        try:
            result = Result.objects.get(id_result=id_pending_result, status='pending')
        except Result.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Update the fields with the input from the request body
        result.id_player_victory = TheUser.objects.get( id_user = request.data.get('id_player_victory') )
        result.status = 'completed'
        result.save()

        # Call the FindTheCompetitionRating method (not implemented here)
        # FindTheCompetitionRating()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCompletedResults(APIView):

    def get(self, request):
        id_user = request.GET.get('id_user')
        if id_user is None:
            return Response({'error': 'id_user is required'}, status=status.HTTP_400_BAD_REQUEST)

        results = Result.objects.filter(
            status='completed',
            id_match__in=Match.objects.filter(Q(id_player_a__id_user=id_user) | Q(id_player_b__id_user=id_user))
        )

        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)

class ViewCompletedResult(APIView):

    def get(self, request, id_completed_result):
        # Get the Result entry
        try:
            result = Result.objects.get(id_result=id_completed_result, status='completed')
        except Result.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ResultSerializer(result)
        return Response(serializer.data)

    def post(self, request, id_completed_result):
        # Get the Result entry
        try:
            result = Result.objects.get(id_result=id_completed_result, status='completed')
        except Result.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Set the status to "pending"
        result.status = 'pending'
        result.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


def set_match_to_rejected( match , id_player_a , id_player_b , date , time ) :

    # 4 different permutations , Match.id_player_a = id_player_a , Match.id_player_b = player_b , Match.id_player_a = id_player_b , Match.id_player_b = id_player_a
    list_one = Match.objects.filter( id_player_a = id_player_a , date = date , start_time = time  )
    list_two = Match.objects.filter(id_player_b=id_player_b, date=date, start_time=time)
    list_three = Match.objects.filter(id_player_a=id_player_b, date=date, start_time=time)
    list_four = Match.objects.filter( id_player_b = id_player_a , date = date , start_time = time )

    print(list_one , list_two , list_three , list_four )

    for x in list_one :
        if x != match :
            x.the_current_status_a = "rejected"
            x.save()

    for x in list_two :

        if x != match :
            x.the_current_status_b = "rejected"
            x.save()

    for x in list_three :

        if x != match :
            x.the_current_status_a = "rejected"
            x.save()

    for x in list_four :
        if x != match :
            x.the_current_status_b = "rejected"
            x.save()

def delete_all_schedule_entry( id_player_a , id_player_b , date , time  ) :

    # 2 different permutations , Schedule.id_user = id_player_a , Schedule.id_user = id_player_b

    list_one = Schedule.objects.filter( id_user = id_player_a , date = date , start_time = time )
    list_two = Schedule.objects.filter( id_user = id_player_b , date = date , start_time = time )

    print(list_one , list_two  )

    for x in list_one :
        x.delete()

    for x in list_two :
        x.delete()

class AcceptMatch(APIView):

    def post(self, request, id_match):

        # Get the match entry with the same id_match as id_match from the url
        try:
            match = Match.objects.get(id_match=id_match)
        except Match.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        id_user = int( request.data['id_user'])
        if id_user == match.id_player_a.id_user:

            if match.the_current_status_a == 'pending' or match.the_current_status_a == 'rejected':
                match.the_current_status_a = 'accepted'
                match.save()

                if match.the_current_status_b == 'accepted':

                    if match.type == 'training':
                        feedback = Feedback(id_match=match , id_player_a = match.id_player_b , id_player_b = match.id_player_a , status='pending')
                        feedback.save()
                        feedback = Feedback(id_match=match , id_player_a = match.id_player_a , id_player_b = match.id_player_b , status='pending')
                        feedback.save()

                    else:
                        the_result = Result(id_match=match, status='pending' , id_player_victory = match.id_player_a )
                        the_result.save()

                    set_match_to_rejected( match , match.id_player_a, match.id_player_b, match.date, match.start_time )
                    delete_all_schedule_entry(match.id_player_a, match.id_player_b, match.date, match.start_time)

        elif id_user == match.id_player_b.id_user:

            if match.the_current_status_b == 'pending' or match.the_current_status_b == 'rejected' :
                match.the_current_status_b = 'accepted'
                match.save()

                if match.the_current_status_a == 'accepted':

                    if match.type == 'training':
                        feedback = Feedback(id_match=match, id_player_a=match.id_player_b, id_player_b=match.id_player_a, status='pending')
                        feedback.save()
                        feedback = Feedback(id_match=match, id_player_a=match.id_player_a, id_player_b=match.id_player_b, status='pending')
                        feedback.save()

                    else:
                        the_result = Result(id_match=match, status='pending' , id_player_victory = match.id_player_a )
                        the_result.save()

                    set_match_to_rejected( match , match.id_player_a, match.id_player_b, match.date, match.start_time )
                    delete_all_schedule_entry( match.id_player_a , match.id_player_b , match.date , match.start_time )

        return Response(status=status.HTTP_200_OK)

class RejectMatch(APIView):

    def post(self, request, id_match):

        try:
            match = Match.objects.get(id_match=id_match)
        except Match.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        id_user = request.data['id_user']

        if id_user == match.id_player_a.id_user:
            match.the_current_status_a = 'rejected'
            match.save()

        if id_user == match.id_player_b.id_user:
            match.the_current_status_b = 'rejected'
            match.save()

        return Response(status=status.HTTP_200_OK)

class DeleteMatch(APIView):

    def post(self, request, id_match):
        try:
            match = Match.objects.get(id_match=id_match)
        except Match.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        id_user = request.data['id_user']

        if id_user == match.id_player_a.id_user:
            if match.the_current_status_a == 'accepted':
                if match.type == 'competitive':
                    match.the_current_status_a = 'deleted'
                    match.save()
                    Result.objects.filter(id_match=match).delete()
                else:
                    match.the_current_status_a = 'deleted'
                    match.save()
                    Feedback.objects.filter(id_match=match).delete()

        if id_user == match.id_player_b.id_user:
            if match.the_current_status_b == 'accepted':
                if match.type == 'competitive':
                    match.the_current_status_b = 'deleted'
                    match.save()
                    Result.objects.filter(id_match=match).delete()

                else:
                    match.the_current_status_b = 'deleted'
                    match.save()
                    Feedback.objects.filter(id_match=match).delete()

        return Response(status=status.HTTP_200_OK)


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Location
from .serializers import LocationNameSerializer

class LocationListView(APIView):
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationNameSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer

class TheRegisterUserView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'user_id': serializer.instance.id,
                'email': serializer.instance.email,
                'name': serializer.instance.name,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# views.py

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserLoginSerializer

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)  # assuming email-based authentication

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class UserLogoutView(APIView):
    def post(self, request):
        # Simply delete the token to force a login
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)
