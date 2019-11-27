from djongo import models

class Team(models.Model):
    team_name = models.CharField(max_length=30)
    school_name = models.CharField(max_length=500)
    #logo?
    def __str__(self):
        return self.team_name

class ScoringType(models.Model):
    name = models.CharField(max_length=40)
    limit = models.IntegerField(default=0)
    value = models.IntegerField()
    extra_data = models.CharField(max_length=10)
    input_style = models.CharField(max_length=15)
    def __str__(self):
        return self.name

class Game(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="team1")
    score1 = models.IntegerField(default=0)
    team2 = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="team2")
    score2 = models.IntegerField(default=0)
    team3 = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="team3")
    score3 = models.IntegerField(default=0)
    team4 = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="team4")
    score4 = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    finished = models.BooleanField(default=False)
    special_name = models.PositiveSmallIntegerField(default=0)
    
class GameParticipant(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    score = models.IntegerField(default=0)
    def __str__(self):
        return ", ".join(["Game " + str(self.game.id), self.team.team_name])
    def score(self):
        counts_list = []
        for scoring_type in ScoringType.objects.all():
            counts_list.append(self.counts(scoring_type))
        return 0
        #return some function of all the counts
    def counts(self, scoring_type):
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
    
class Action(models.Model):
    scoring_type = models.ForeignKey(ScoringType, on_delete=models.DO_NOTHING)
    time = models.DateTimeField()
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    multiplier = models.FloatField(default=1)
    upDown = models.BooleanField(default=1)
    deleted = models.BooleanField(default=False)
    def __str__(self):
        return ", ".join(["Game " + str(self.game.id), str(self.scoring_type), str(self.team)])