# Generated by Django 2.2.7 on 2019-11-11 05:35

from django.db import migrations
from django.utils import timezone
from team_management.models import ScoringType, Team, Game, GameParticipant

def initializeDb(apps, schema_editor):
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
    
    from django.contrib.auth.models import User
    superuser = User.objects.create_superuser(
        username = "MRDC",
        email = "test@test.com",
        password = "password", #Obviously don't leave this as is
        )
    
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType

    content_type = ContentType.objects.get_for_model(Game)
    judge_perm = Permission.objects.create(
        codename='is_judge',
        name='is_judge',
        content_type=content_type,)
    
    judge = User.objects.create_user('judge', 'test@test.com', 'password')
    judge.user_permissions.add(judge_perm)
    judge.save() #needs save for the permission
    
    audience = User.objects.create_user('Audience', 'test@test.com', 'password') #No permissions
    Team.objects.create(user=audience,  team_name='Audience', school_name='N/A', abbr='Audience', capt_name='N/A')
    
    content_type = ContentType.objects.get_for_model(Team)
    team_perm = Permission.objects.create(
        codename='is_team',
        name='is_team',
        content_type=content_type,)
    
    import csv
    import random

    with open('/code/TeamData.csv', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, dialect='excel')
        s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        passlen = 15
        for team in csvreader:
            password = "".join(random.sample(s, passlen))
            user = User.objects.create_user(team['Name'], team['Email'], password)
            Team.objects.create(user=user,  team_name=team['Name'], school_name=team['School'], abbr=team['Abbr'], capt_name=team['Captain Name'])
            user.user_permissions.add(team_perm)
            user.save()
    
    testTeamUser = User.objects.create_user('MRDCTestTeam', 'test@test.com', "password")
    Team.objects.create(user=testTeamUser,  team_name='MRDCTestTeam', school_name='UIUC', abbr='MRDCTT', capt_name='Michael Gale')
    testTeamUser.user_permissions.add(team_perm)
    testTeamUser.save()
    
class Migration(migrations.Migration):

    dependencies = [
        ('team_management', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initializeDb),
    ]
