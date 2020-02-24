from django.db import models
from django.db.models import Sum
from django.utils import timezone

class Team(models.Model):
    team_name = models.CharField(max_length=30)
    school_name = models.CharField(max_length=500)
    #logo?
    def __str__(self):
        return self.team_name

class ScoringType(models.Model): #Table for every way to score. #Autogenerates buttons on the judging page
    name = models.CharField(max_length=40)
    limit = models.IntegerField(default=0)
    value = models.IntegerField()
    extra_data = models.CharField(max_length=10) #used to set colors on the judging page for counters
    input_style = models.CharField(max_length=15) #specifies how the judging screen should display it
    def __str__(self):
        return self.name

class Game(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    finished = models.BooleanField(default=False)
    special_name = models.PositiveSmallIntegerField(default=0) #stores data for special games. ie. 1 means it is a semifinal #not used yet
    
class GameParticipant(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    score = models.IntegerField(default=0)
    def __str__(self):
        return ", ".join(["Game " + str(self.game.id), self.team.team_name])
        
    def calculateScore(self): #updates score field #Unfinished
        sum = 0
        for scoring_type in ScoringType.objects.all(): #loops through each scoring_type
            if scoring_type.value != 0:
                for count_mult in self.counts(scoring_type): #repeats for each multiplier level
                    sum += scoring_type.value * count_mult[0] * count_mult[1] #value * count * multiplier
            else:
                sum += self.switcher.get(scoring_type.name)(self, self.counts(scoring_type)) #calls custom function if scoring_type.value == 0
        #saves score to db
        self.score = sum
        self.save()
        return sum

    def brewPotion(self, countslist):
        i=0
        total=0
        for count_mult in countslist:
            while count_mult[0] > 0:
                total += (20 + i*10) * count_mult[1] #custom formula
                i+=1
                count_mult[0] -= 1
        return total
        
    def counts(self, scoring_type): #Outputs a list of pairs [count, multiplier] for that scoringType; Pairs come in chronological order with each multiplier level grouped
        base = Action.objects.filter(
                deleted = False
            ).filter(
                game_participant = self.id
            ).filter(
                scoring_type = scoring_type
            )
        counts_multipliers = []
        for mults in base.values('multiplier').distinct():
            count = base.filter(
                    multiplier = mults['multiplier']
                ).aggregate(Sum('value', output_field=models.IntegerField()))['value__sum'] #sums over the value field to count for regular buttons, or read a single value for others
            counts_multipliers.append([count, mults['multiplier']])
        return counts_multipliers
        
    switcher = {
        "Brew Potion":brewPotion,
    }
    
class Action(models.Model): #Table for every scoring action
    scoring_type = models.ForeignKey(ScoringType, on_delete=models.CASCADE)
    game_participant = models.ForeignKey(GameParticipant, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now())
    multiplier = models.FloatField(default=1)
    value = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    def __str__(self):
        return ", ".join(["Game " + str(self.game_participant.game_id), str(self.scoring_type), str(self.game_participant.team)])
