from django.db import models

class Location(models.Model):
    id_location = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    the_address = models.CharField(max_length=255)
    table_number = models.IntegerField()

"""class TheUser(models.Model):
    id_user = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    forehand_rubber_type = models.CharField(max_length=255, choices=[('short or long pimples', 'short or long pimples'), ('inverted', 'inverted')])
    backhand_rubber_type = models.CharField(max_length=255, choices=[('short or long pimples', 'short or long pimples'), ('inverted', 'inverted')])
    competition_rating = models.IntegerField()
    real_world_rating = models.IntegerField()
    serve_feedback = models.FloatField()
    receive_feedback = models.FloatField()
    forehand_loop_feedback = models.FloatField()
    backhand_loop_feedback = models.FloatField()
    forehand_block_feedback = models.FloatField()
    backhand_block_feedback = models.FloatField()
    personal_feedback = models.FloatField()

    class Meta:
        db_table = 'new_schedule_and_match_user'"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, name, last_name):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, name, last_name):
        user = self.create_user(email, password, name, last_name)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class TheUser(AbstractBaseUser, PermissionsMixin):
    id_user = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # ... [rest of your fields here]

    forehand_rubber_type = models.CharField(max_length=255, choices=[('short or long pimples', 'short or long pimples'),('inverted', 'inverted')],  default = ('inverted', 'inverted'))
    backhand_rubber_type = models.CharField(max_length=255, choices=[('short or long pimples', 'short or long pimples'),('inverted', 'inverted')] , default = ('inverted', 'inverted'))
    competition_rating = models.IntegerField( default = 1 )
    real_world_rating = models.IntegerField( default = 1 )
    serve_feedback = models.FloatField(default = 1 )
    receive_feedback = models.FloatField(default = 1 )
    forehand_loop_feedback = models.FloatField(default = 1 )
    backhand_loop_feedback = models.FloatField(default = 1 )
    forehand_block_feedback = models.FloatField(default = 1 )
    backhand_block_feedback = models.FloatField(default = 1 )
    personal_feedback = models.FloatField(default = 1 )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # for admin access
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name']

    class Meta:
        db_table = 'new_schedule_and_match_user'


class Match(models.Model):
    id_match = models.AutoField(primary_key=True)
    id_player_a = models.ForeignKey(TheUser, related_name='player_a', on_delete=models.CASCADE)
    id_player_b = models.ForeignKey(TheUser, related_name='player_b', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    the_current_status_a = models.CharField(max_length=255, choices=[('pending', 'pending'), ('accepted', 'accepted'), ('rejected', 'rejected'), ('deleted', 'deleted')])
    the_current_status_b = models.CharField(max_length=255, choices=[('pending', 'pending'), ('accepted', 'accepted'), ('rejected', 'rejected'), ('deleted', 'deleted')])
    date = models.DateField()
    type = models.CharField(max_length=255, choices=[('training', 'training'), ('competitive', 'competitive')])
    start_time = models.IntegerField(choices=[(i, i) for i in range(6, 21)])

class Feedback(models.Model):
    id_feedback = models.AutoField(primary_key=True)
    id_match = models.ForeignKey(Match, on_delete=models.CASCADE)
    id_player_a = models.ForeignKey(TheUser, related_name='feedback_player_a', on_delete=models.CASCADE)
    id_player_b = models.ForeignKey(TheUser, related_name='feedback_player_b', on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=[('pending', 'pending'), ('completed', 'completed')] )
    serve_feedback = models.IntegerField(choices=[(i, i) for i in range(1, 11)] , default = 1 )
    receive_feedback = models.IntegerField(choices=[(i, i) for i in range(1, 11)] , default = 1 )
    forehand_loop_feedback = models.IntegerField(choices=[(i, i) for i in range(1, 11)] , default = 1 )
    backhand_loop_feedback = models.IntegerField(choices=[(i, i) for i in range(1, 11)] , default = 1 )
    forehand_block_feedback = models.IntegerField(choices=[(i, i) for i in range(1, 11)] , default = 1 )
    backhand_block_feedback = models.IntegerField(choices=[(i, i) for i in range(1, 11)] , default = 1 )
    personal_feedback = models.IntegerField(choices=[(i, i) for i in range(1, 11)] , default = 1 )

class Result(models.Model):
    id_result = models.AutoField(primary_key=True)
    id_match = models.ForeignKey(Match, on_delete=models.CASCADE)
    id_player_victory = models.ForeignKey(TheUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=[('pending', 'pending'), ('completed', 'completed')])

class Schedule(models.Model):
    id_schedule = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(TheUser, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=255, choices=[('training', 'training'), ('competitive', 'competitive')])
    start_time = models.IntegerField(choices=[(i, i) for i in range(6, 21)])


