# Generated by Django 2.2.7 on 2019-11-11 05:35

from django.db import migrations
from django.utils import timezone
from team_management.models import ScoringType, Team, Game, GameParticipant


def initializeDb(apps, schema_editor):
    Team.objects.create(team_name="Lion", school_name="UIUC")
    Team.objects.create(team_name="Phoenix", school_name="Valpo")
    Team.objects.create(team_name="Hydra", school_name="IIT")
    Team.objects.create(team_name="Unicorn", school_name="College of Dupage")
    
    ScoringType.objects.create(name="Green Dragon ball", limit=0, value=16, extra_data="#00FF00", input_style="Counter")
    ScoringType.objects.create(name="Blue Dragon ball", limit=0, value=16, extra_data="#0000FF", input_style="Counter")
    ScoringType.objects.create(name="Red Dragon ball", limit=0, value=12, extra_data="#FF0000", input_style="Counter")
    ScoringType.objects.create(name="Purple Dragon ball", limit=0, value=8, extra_data="#9400D3", input_style="Counter")
    ScoringType.objects.create(name="Yellow Dragon ball", limit=0, value=8, extra_data="#FFFF00", input_style="Counter")
    ScoringType.objects.create(name="Orange Dragon ball", limit=0, value=-12, extra_data="#FFA500", input_style="Counter")
    ScoringType.objects.create(name="Pink Dragon ball", limit=0, value=-12, extra_data="#ffc0cb", input_style="Counter")
    
    ScoringType.objects.create(name="Brew Potion", limit=3, value=0, extra_data="", input_style="Standard")
    ScoringType.objects.create(name="Open Treasury", limit=1, value=10, extra_data="", input_style="Standard")
    ScoringType.objects.create(name="Infinite Example", limit=0, value=1, extra_data="", input_style="Standard")
    ScoringType.objects.create(name="Dragon Egg", limit=2, value=40, extra_data="", input_style="Standard")
    ScoringType.objects.create(name="Broken Dragon Egg", limit=2, value=10, extra_data="", input_style="Standard")

    ScoringType.objects.create(name="Green Treasure ball", limit=0, value=4, extra_data="#00FF00", input_style="Counter2")
    ScoringType.objects.create(name="Blue Treasure ball", limit=0, value=4, extra_data="#0000FF", input_style="Counter2")
    ScoringType.objects.create(name="Red Treasure ball", limit=0, value=3, extra_data="#FF0000", input_style="Counter2")
    ScoringType.objects.create(name="Purple Treasure ball", limit=0, value=2, extra_data="#9400D3", input_style="Counter2")
    ScoringType.objects.create(name="Yellow Treasure ball", limit=0, value=2, extra_data="#FFFF00", input_style="Counter2")
    ScoringType.objects.create(name="Orange Treasure ball", limit=0, value=-3, extra_data="#FFA500", input_style="Counter2")
    ScoringType.objects.create(name="Pink Treasure ball", limit=0, value=-3, extra_data="#ffc0cb", input_style="Counter2")
    
    Game.objects.create(start_time=timezone.now(), end_time=timezone.now())
    
    GameParticipant.objects.create(team = Team.objects.get(pk=1), game = Game.objects.get(pk=1))
    GameParticipant.objects.create(team = Team.objects.get(pk=2), game = Game.objects.get(pk=1))
    GameParticipant.objects.create(team = Team.objects.get(pk=3), game = Game.objects.get(pk=1))
    GameParticipant.objects.create(team = Team.objects.get(pk=4), game = Game.objects.get(pk=1))
    
    from django.contrib.auth.models import User
    superuser = User.objects.create_superuser(
        username = "MRDC",
        email = "test@test.com",
        password = "password", #Obviously don't leave this as is
        )
    
class Migration(migrations.Migration):

    dependencies = [
        ('team_management', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initializeDb),
    ]
