# Generated by Django 2.2.7 on 2019-11-11 05:35

from django.db import migrations
from django.utils import timezone

from team_management.models import School, Team, ScoringTypeGroup, ScoringType, ScoringEvent

def initializeDb(apps, schema_editor):
    counter_arrows = ScoringTypeGroup.objects.create(name="Text and Arrows")
    ScoringType.objects.create(name="Green Dragon ball", limit=0, score_change=16, extra_data="#00FF00", scoring_type_group=counter_arrows)
    ScoringType.objects.create(name="Blue Dragon ball", limit=0, score_change=16, extra_data="#0000FF", scoring_type_group=counter_arrows)
    ScoringType.objects.create(name="Red Dragon ball", limit=0, score_change=12, extra_data="#FF0000", scoring_type_group=counter_arrows)
    ScoringType.objects.create(name="Purple Dragon ball", limit=0, score_change=8, extra_data="#9400D3", scoring_type_group=counter_arrows)
    ScoringType.objects.create(name="Yellow Dragon ball", limit=0, score_change=8, extra_data="#FFFF00", scoring_type_group=counter_arrows)
    ScoringType.objects.create(name="Orange Dragon ball", limit=0, score_change=-12, extra_data="#FFA500", scoring_type_group=counter_arrows)
    ScoringType.objects.create(name="Pink Dragon ball", limit=0, score_change=-12, extra_data="#ffc0cb", scoring_type_group=counter_arrows)
    
    standard_button = ScoringTypeGroup.objects.create(name="Standard Buttons")
    ScoringType.objects.create(name="Brew Potion", limit=3, score_change=0, extra_data="", scoring_type_group=standard_button)
    ScoringType.objects.create(name="Open Treasury", limit=1, score_change=10, extra_data="", scoring_type_group=standard_button)
    ScoringType.objects.create(name="Infinite Example", limit=0, score_change=1, extra_data="", scoring_type_group=standard_button)
    ScoringType.objects.create(name="Dragon Egg", limit=2, score_change=40, extra_data="", scoring_type_group=standard_button)
    ScoringType.objects.create(name="Broken Dragon Egg", limit=2, score_change=10, extra_data="", scoring_type_group=standard_button)
    
    counter_arrows_box = ScoringTypeGroup.objects.create(name="Text and Arrows_Box")
    ScoringType.objects.create(name="Green Treasure ball", limit=0, score_change=4, extra_data="#00FF00", scoring_type_group=counter_arrows_box)
    ScoringType.objects.create(name="Blue Treasure ball", limit=0, score_change=4, extra_data="#0000FF", scoring_type_group=counter_arrows_box)
    ScoringType.objects.create(name="Red Treasure ball", limit=0, score_change=3, extra_data="#FF0000", scoring_type_group=counter_arrows_box)
    ScoringType.objects.create(name="Purple Treasure ball", limit=0, score_change=2, extra_data="#9400D3", scoring_type_group=counter_arrows_box)
    ScoringType.objects.create(name="Yellow Treasure ball", limit=0, score_change=2, extra_data="#FFFF00", scoring_type_group=counter_arrows_box)
    ScoringType.objects.create(name="Orange Treasure ball", limit=0, score_change=-3, extra_data="#FFA500", scoring_type_group=counter_arrows_box)
    ScoringType.objects.create(name="Pink Treasure ball", limit=0, score_change=-3, extra_data="#ffc0cb", scoring_type_group=counter_arrows_box)
    

    from django.contrib.auth.models import User
    superuser = User.objects.create_superuser(
        username = "MRDC",
        email = "test@test.com",
        password = "password", #Obviously don't leave this as is
        )
    
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType

    content_type = ContentType.objects.get_for_model(ScoringEvent)
    judge_perm = Permission.objects.create(
        codename='is_judge',
        name='is_judge',
        content_type=content_type,)
    
    judge = User.objects.create_user('judge', 'test@test.com', 'password')
    judge.user_permissions.add(judge_perm)
    judge.save() #needs save for the permission
    
    ''' idk how we want to refactor and handle the audience now. The main goal of their user 
    # was to have it show up as an option to adding phone numbers,
    # but that had a lot of downstream consequences with it showing up elsewhere too
    audience = User.objects.create_user('Audience', 'test@test.com', 'password') #No permissions
    Team.objects.create(user=audience,  team_name='Audience', school_name='N/A', abbr='Audience', capt_name='N/A')
    '''
    
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
            school = School.objects.create(name=team['School'], abbreviation=team['School'][0:8])
            Team.objects.create(user=user, name=team['Name'], school=school, abbreviation=team['Abbr'])
            '''
            Email teams their password
            '''
            user.user_permissions.add(team_perm)
            user.save()
    
    testTeamUser = User.objects.create_user('MRDCTestTeam', 'test@test.com', "password")
    test_school = School.objects.create(name='Test School', abbreviation='TEST')
    Team.objects.create(user=testTeamUser, name='MRDCTestTeam', school=test_school, abbreviation='MRDCTT')
    testTeamUser.user_permissions.add(team_perm)
    testTeamUser.save()
    
class Migration(migrations.Migration):

    dependencies = [
        ('team_management', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initializeDb),
    ]
