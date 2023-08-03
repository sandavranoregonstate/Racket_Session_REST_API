from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

from .models import ScheduleToDrill

class ScheduleToDrillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleToDrill
        fields = '__all__'
