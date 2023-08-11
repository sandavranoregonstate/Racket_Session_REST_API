from rest_framework.parsers import JSONParser
from .models import TheUser , Schedule, Location , Match , ScheduleToDrill , Drill , Result , MatchToDrill , Feedback
from .serializers import ScheduleToDrillSerializer , ResultSerializer ,  MatchSerializer , FeedbackSerializer

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

        # Create the “Schedule” entry using the data from the input, except the drill list
        schedule = Schedule(id_user= TheUser.objects.get( id_user = id_user ), location=location, date=date, type=type, start_time=start_time)
        schedule.save()

        # Create the ScheduleToDrill entries
        drills = request.data.get('drills', [])
        for drill_string in drills:
            drill = Drill.objects.get(explanation=drill_string)
            schedule_to_drill_data = {
                'id_drill': drill.id_drill,
                'id_schedule': schedule.id_schedule
            }
            schedule_to_drill_serializer = ScheduleToDrillSerializer(data=schedule_to_drill_data)
            if schedule_to_drill_serializer.is_valid():
                schedule_to_drill_serializer.save()
            else:
                return Response(schedule_to_drill_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Call the Pair method (not implemented here)
        # pair()

        return Response(status=status.HTTP_201_CREATED)




class ViewSchedule(APIView):

    parser_classes = (JSONParser,)

    def get(self, request, id_schedule):
        # Get the schedule entry with the same id_schedule as id_schedule from the URL
        try:
            schedule = Schedule.objects.get(id_schedule=id_schedule)
        except Schedule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Get a list of “ScheduleToDrill” entry with the same id_schedule as id_schedule from the URL
        schedule_to_drills = ScheduleToDrill.objects.filter(id_schedule=schedule)

        # Get a list of “Drill” entry with the same id_drill as id_drill from the given list of the “ScheduleToDrill” entry
        drills = [Drill.objects.get(id_drill=std.id_drill.id_drill) for std in schedule_to_drills]

        # Prepare the response data
        response_data = {
            'Schedule': {
                'id_schedule': id_schedule,
                'location': schedule.location.name,
                'date': schedule.date,
                'type': schedule.type,
                'start_time': 10
            },
            'Drills': [
                {
                    'id_drill': drill.id_drill,
                    'explanation': drill.explanation
                }
                for drill in drills
            ]
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



class ListMatch(APIView):

    def get(self, request):
        id_user = request.GET.get('id_user')
        if id_user is None:
            return Response({'error': 'id_user is required'}, status=status.HTTP_400_BAD_REQUEST)

        matches = Match.objects.filter(Q(id_player_a=id_user) | Q(id_player_b=id_user))
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)




class ViewMatch(APIView):

    def get(self, request, id_match):
        # Get the Match entry
        try:
            match = Match.objects.get(id_match=id_match)
        except Match.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Get the list of MatchToDrill entries
        match_to_drills = MatchToDrill.objects.filter(id_match=id_match)

        drills = [Drill.objects.get(id_drill=std.id_drill.id_drill) for std in match_to_drills]

        # Prepare the response data
        response_data = {
            'Match': {
                "id_match" : id_match ,
                'id_player_a': match.id_player_a.id_user,
                'id_player_b': match.id_player_b.id_user,
                'location': match.location.id_location,
                'the_current_status_a': match.the_current_status_a,
                'the_current_status_b': match.the_current_status_b ,
                "date" : match.date ,
                "type" : match.type ,
                "start_time" : 10
            },
            'Drills': [
                {
                    'id_drill': drill.id_drill,
                    'explanation': drill.explanation
                }
                for drill in drills
            ]
        }


        print( response_data )
        # Return the “Schedule” entry and list of “Drill” entry
        return Response(response_data, status=status.HTTP_200_OK)



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

            if match.the_current_status_a == 'pending':
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

            if match.the_current_status_b == 'pending':
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

