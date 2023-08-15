from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

from .models import Match

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'
        depth = 4

from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        depth = 3

from .models import Result

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
        depth = 3

from .models import Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

from .models import TheUser

class TheUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheUser
        fields = '__all__'

# serializers.py
from rest_framework import serializers
from .models import Location

class LocationNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('name',)

# serializers.py

from rest_framework import serializers
from .models import TheUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheUser
        fields = ['email', 'password', 'name', 'last_name' ]  # Add other fields as necessary.
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = TheUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


# serializers.py

from rest_framework import serializers

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


