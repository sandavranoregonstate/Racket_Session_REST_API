# Generated by Django 4.2.2 on 2023-08-03 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("new_schedule_and_match", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="User",
            new_name="TheUser",
        ),
    ]
