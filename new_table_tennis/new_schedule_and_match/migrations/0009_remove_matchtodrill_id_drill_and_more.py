# Generated by Django 4.2.2 on 2023-08-14 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "new_schedule_and_match",
            "0008_alter_feedback_backhand_block_feedback_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="matchtodrill",
            name="id_drill",
        ),
        migrations.RemoveField(
            model_name="matchtodrill",
            name="id_match",
        ),
        migrations.RemoveField(
            model_name="matchtodrill",
            name="id_player",
        ),
        migrations.RemoveField(
            model_name="scheduletodrill",
            name="id_drill",
        ),
        migrations.RemoveField(
            model_name="scheduletodrill",
            name="id_schedule",
        ),
        migrations.DeleteModel(
            name="Drill",
        ),
        migrations.DeleteModel(
            name="MatchToDrill",
        ),
        migrations.DeleteModel(
            name="ScheduleToDrill",
        ),
    ]
