from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .models import Schedule
from .serializers import ScheduleSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Drill, ScheduleToDrill
from .serializers import ScheduleToDrillSerializer

class ListSchedule(APIView):
    parser_classes = (JSONParser,)

    def get(self, request ):
        id_user = request.GET.get('id_user')
        schedules = Schedule.objects.filter(id_user=id_user)
        serializer = ScheduleSerializer(schedules, many=True)
        return Response({'items': serializer.data})

    def post(self, request):
        # Create the Schedule entry
        schedule_serializer = ScheduleSerializer(data=request.data)
        if schedule_serializer.is_valid():
            schedule = schedule_serializer.save()
        else:
            return Response(schedule_serializer.errors, status=status.HTTP_404_BAD_REQUEST)

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
        # Get the Schedule entry
        try:
            schedule = Schedule.objects.get(id_schedule=id_schedule)
        except Schedule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Get the list of ScheduleToDrill entries
        schedule_to_drills = ScheduleToDrill.objects.filter(id_schedule=id_schedule)
        schedule_serializer = ScheduleSerializer(schedule)
        schedule_to_drill_serializer = ScheduleToDrillSerializer(schedule_to_drills, many=True)

        return Response({
            'Schedule': schedule_serializer.data,
            'ScheduleToDrill': schedule_to_drill_serializer.data
        })

    def delete(self, request, id_schedule):
        try:
            schedule = Schedule.objects.get(id_schedule=id_schedule)
        except Schedule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.db.models import Q
from .models import Match
from .serializers import MatchSerializer

class ListMatch(APIView):

    def get(self, request):
        id_user = request.GET.get('id_user')
        if id_user is None:
            return Response({'error': 'id_user is required'}, status=status.HTTP_400_BAD_REQUEST)

        matches = Match.objects.filter(Q(id_player_a=id_user) | Q(id_player_b=id_user))
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)


from .models import MatchToDrill
from .serializers import MatchToDrillSerializer

class ViewMatch(APIView):

    def get(self, request, id_match):
        # Get the Match entry
        try:
            match = Match.objects.get(id_match=id_match)
        except Match.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Get the list of MatchToDrill entries
        match_to_drills = MatchToDrill.objects.filter(id_match=id_match)
        match_serializer = MatchSerializer(match)
        match_to_drill_serializer = MatchToDrillSerializer(match_to_drills, many=True)

        return Response({
            'Match': match_serializer.data,
            'MatchToDrill': match_to_drill_serializer.data
        })

from .models import Feedback
from .serializers import FeedbackSerializer

class ListPendingFeedback(APIView):

    def get(self, request):
        id_user = request.GET.get('id_user')
        if id_user is None:
            return Response({'error': 'id_user is required'}, status=status.HTTP_400_BAD_REQUEST)

        feedbacks = Feedback.objects.filter(Q(id_player_a=id_user) | Q(id_player_b=id_user), status='pending')
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response({'items': serializer.data})

class ViewPendingFeedback(APIView):

    def get(self, request, id_pending_feedback):
        # Get the Feedback entry
        try:
            feedback = Feedback.objects.get(id_feedback=id_pending_feedback, status='pending')
        except Feedback.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data)

class SubmitFeedback(APIView):

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

from .models import Feedback
from .serializers import FeedbackSerializer

class ListCompletedFeedback(APIView):

    def get(self, request):
        id_user = request.GET.get('id_user')
        if id_user is None:
            return Response({'error': 'id_user is required'}, status=status.HTTP_400_BAD_REQUEST)

        feedbacks = Feedback.objects.filter(Q(id_player_a=id_user) | Q(id_player_b=id_user), status='completed')
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response({'items': serializer.data})
