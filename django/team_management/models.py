from djongo import models

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
    def score(self): #updates score field #Unfinished
        counts_list = []
        for scoring_type in ScoringType.objects.all():
            counts_list.append(self.counts(scoring_type))
        return 0
        #return some function of all the counts
    def counts(self, scoring_type): #Outputs a list of tuples (count, multiplier) for that scoringType
        base = Action.objects.filter(
                deleted = False
            ).filter(
                team = self.team
            ).filter(
                scoring_type = scoring_type
            )
        counts_multipliers = []
        print(base.values('multiplier').distinct())
        for mult in base.values('multiplier').distinct():
            mult_table = base.filter(multiplier = mult['multiplier'])
            up = mult_table.filter(
                    upDown = True
                ).count()
            down = mult_table.filter( #note only counter style inputs have any "down" values
                    upDown = False
                ).count()
            counts_multipliers.append((up-down, mult['multiplier']))
        return counts_multipliers
    
class Action(models.Model): #Table for every scoring action
    scoring_type = models.ForeignKey(ScoringType, on_delete=models.CASCADE)
    time = models.DateTimeField()
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    multiplier = models.FloatField(default=1)
    upDown = models.BooleanField(default=1) #True is up
    deleted = models.BooleanField(default=False)
    def __str__(self):
        return ", ".join(["Game " + str(self.game.id), str(self.scoring_type), str(self.team)])