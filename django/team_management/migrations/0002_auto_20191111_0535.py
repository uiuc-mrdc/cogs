# Generated by Django 2.2.7 on 2019-11-11 05:35

from django.db import migrations
from team_management.models import Action, ScoringType, Team


def initializeDb(apps, schema_editor):
    Team.objects.create(team_name="Mechabytes", school_name="UIUC")
    Team.objects.create(team_name="Marvin", school_name="Valpo")
    Team.objects.create(team_name="ITR Roslund", school_name="IIT")
    Team.objects.create(team_name="Scotty Bees", school_name="College of Dupage")
    
    ScoringType.objects.create(name="Red Dragon ball", limit=0, value=16, extra_data="#FF0000", input_style="Counter")
    ScoringType.objects.create(name="Blue Dragon ball", limit=0, value=16, extra_data="#0000FF", input_style="Counter")
    ScoringType.objects.create(name="Green Dragon ball", limit=0, value=16, extra_data="#00FF00", input_style="Counter")
    
    ScoringType.objects.create(name="Brew Potion", limit=3, value=30, extra_data="", input_style="Standard")
    ScoringType.objects.create(name="Open Treasury", limit=1, value=40, extra_data="", input_style="Standard")
    ScoringType.objects.create(name="Infinite Example", limit=0, value=1, extra_data="", input_style="Standard")

class Migration(migrations.Migration):

    dependencies = [
        ('team_management', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initializeDb),
    ]
