from django.db import models

class Location(models.Model):
    id_location = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    the_address = models.CharField(max_length=255)
    table_number = models.IntegerField()

class User(models.Model):
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

class Match(models.Model):
    id_match = models.AutoField(primary_key=True)
    id_player_a = models.ForeignKey(User, related_name='player_a', on_delete=models.CASCADE)
    id_player_b = models.ForeignKey(User, related_name='player_b', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    the_current_status_a = models.CharField(max_length=255, choices=[('pending', 'pending'), ('accepted', 'accepted'), ('rejected', 'rejected'), ('deleted', 'deleted')])
    the_current_status_b = models.CharField(max_length=255, choices=[('pending', 'pending'), ('accepted', 'accepted'), ('rejected', 'rejected'), ('deleted', 'deleted')])
    date = models.DateField()
    type = models.CharField(max_length=255, choices=[('training', 'training'), ('competitive', 'competitive')])
    start_time = models.IntegerField(choices=[(i, i) for i in range(6, 21)])

class Feedback(models.Model):
    id_feedback = models.AutoField(primary_key=True)
    id_match = models.ForeignKey(Match, on_delete=models.CASCADE)
    id_player_a = models.ForeignKey(User, related_name='feedback_player_a', on_delete=models.CASCADE)
    id_player_b = models.ForeignKey(User, related_name='feedback_player_b', on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=[('pending', 'pending'), ('completed', 'completed')])
    serve_feedback = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    receive_feedback = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    forehand_loop_feedback = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    backhand_loop_feedback = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    forehand_block_feedback = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    backhand_block_feedback = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    personal_feedback = models.IntegerField(choices=[(i, i) for i in range(1, 11)])

class Result(models.Model):
    id_result = models.AutoField(primary_key=True)
    id_match = models.ForeignKey(Match, on_delete=models.CASCADE)
    id_player_victory = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=[('pending', 'pending'), ('completed', 'completed')])

class Schedule(models.Model):
    id_schedule = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=255, choices=[('training', 'training'), ('competitive', 'competitive')])
    start_time = models.IntegerField(choices=[(i, i) for i in range(6, 21)])

class Drill(models.Model):
    id_drill = models.AutoField(primary_key=True)
    explanation = models.CharField(max_length=255)

class ScheduleToDrill(models.Model):
    id_schedule_to_drill = models.AutoField(primary_key=True)
    id_drill = models.ForeignKey(Drill, on_delete=models.CASCADE)
    id_schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

class MatchToDrill(models.Model):
    id_match_to_drill = models.AutoField(primary_key=True)
    id_drill = models.ForeignKey(Drill, on_delete=models.CASCADE)
    id_match = models.ForeignKey(Match, on_delete=models.CASCADE)
    id_player = models.ForeignKey(User, on_delete=models.CASCADE)
