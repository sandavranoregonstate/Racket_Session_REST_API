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

