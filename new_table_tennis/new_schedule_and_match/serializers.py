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


from .models import Match

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

from .models import MatchToDrill

class MatchToDrillSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchToDrill
        fields = '__all__'

from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

