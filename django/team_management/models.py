from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class School(models.Model):
    name = models.CharField(max_length=70)
    abbreviation = models.CharField(max_length=8, default="", blank=True)
    logo = models.ImageField(upload_to='logos/schools', blank=True)
    def __str__(self):
        return self.name

class Team(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    abbreviation = models.CharField(max_length=8, default="", blank=True)
    weigh_in = models.BooleanField(default=False)
    safety_check = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='logos/teams', blank=True)
    def __str__(self):
        return self.name

class TeamContact(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
	#regex source: Brooke's comment on https://stackoverflow.com/questions/123559/how-to-validate-phone-numbers-using-regex
	#We may want to update this to match whatever texting service we use, or to be more strict
    phone_number = models.CharField(max_length=15, blank=True, validators=[RegexValidator(regex='(?:(?:(\s*\(?([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\)?\s*(?:[.-]\s*)?)([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})')])


def default_match_time(): #remove default value once we have a way to set this better
    return timezone.now() + timedelta(minutes=10)
class Match(models.Model):
    special_name = models.CharField(max_length=50, default="", blank=True, help_text="i.e. Semifinal. Currently unused")
    scheduled_start = models.DateTimeField(default = default_match_time) #remove default value once we have a way to set this better
    class Meta:
        verbose_name_plural = "Matches"

class MatchStateChangeEvent(models.Model):
    timestamp = models.DateTimeField(default = timezone.now)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    STARTED = 'STA'
    PAUSED = 'PAU'
    RESUMED = 'RES'
    END = 'END'
    FINALIZED = 'FIN'
    EVENT_TYPE_CHOICES = [
        (STARTED, 'Started'), #(stored value, human-readable)
        (PAUSED, 'Paused'),
        (RESUMED, 'Resumed'),
        (END, 'End'),
        (FINALIZED, 'Finalized'),
    ]
    event_type = models.CharField(
        max_length=3,
        choices=EVENT_TYPE_CHOICES,
        default=STARTED,
    )

class ContenderPosition(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=7)
    def __str__(self):
        return self.name
    
class Contender(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='contenders')
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    contender_position = models.ForeignKey(ContenderPosition, on_delete=models.CASCADE)
    def __str__(self):
        return ", ".join(["Match " + str(self.match.id), self.team.name])
    def calculate_score(self): #updates score field #Unfinished
        return 5

class ScoringContext(models.Model):
    multiplier = models.FloatField(default=1)
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name
    
class ContenderContextChangeEvent(models.Model):
    contender = models.ForeignKey(Contender, on_delete=models.CASCADE)
    scoring_context = models.ForeignKey(ScoringContext, on_delete=models.CASCADE)
    match_timestamp = models.DurationField(default=timedelta(minutes=0))
    
    ADD = 'ADD'
    REMOVE = 'REM'
    CHANGE_CHOICES = [
        (ADD, 'Add'),
        (REMOVE, 'Remove'),
    ]
    change = models.CharField(
        max_length=3,
        choices=CHANGE_CHOICES,
        default=ADD,
    )

class ScoringTypeGroup(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name
    
class ScoringType(models.Model): #Table for every way to score. #Autogenerates buttons on the judging page
    name = models.CharField(max_length=40)
    limit = models.IntegerField(default=0, help_text="Maximum number of times this can be scored. 0 for no limit.")
    score_change = models.IntegerField()
    extra_data = models.CharField(max_length=10, blank=True, help_text="Used to display extra things, such as color on the judging page") #used to set colors on the judging page for counters
    scoring_type_group = models.ForeignKey(ScoringTypeGroup, on_delete=models.CASCADE, help_text="Used to group ScoringTypes into display groups for the judging page") #specifies how the judging screen should display it
    def __str__(self):
        return self.name
    
class ScoringEvent(models.Model): #Table for every scoring event
    scoring_type = models.ForeignKey(ScoringType, on_delete=models.CASCADE)
    contender = models.ForeignKey(Contender, on_delete=models.CASCADE)
    match_timestamp = models.DurationField(default=timedelta(minutes=0))
    count = models.IntegerField(default=1)
    def __str__(self):
        return " | ".join(["Match " + str(self.contender.match_id), str(self.scoring_type), str(self.contender.team)])
