from djongo import models

class Team(models.Model):
    team_name = models.CharField(max_length=100)
    school_name = models.CharField(max_length=200)
    def __str__(self):
        return self.team_name

class ScoringType(models.Model):
    name = models.CharField(max_length=40)
    limit = models.IntegerField(default=0)
    value = models.IntegerField()
    extra_data = models.CharField(max_length=20)
    input_group = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class LiveScore(models.Model):
    scoring_type = models.ForeignKey(ScoringType, on_delete=models.DO_NOTHING)
    time = models.DateTimeField('date published')
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    def __str__(self):
        return ", ".join([str(self.scoring_type),str(self.team)])

class Game(models.Model):
    teamOne = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="team1")
    score1 = models.IntegerField(default=0)
    team2 = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="team2")
    score2 = models.IntegerField(default=0)
    team3 = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="team3")
    score3 = models.IntegerField(default=0)
    team4 = models.ForeignKey(Team, on_delete=models.DO_NOTHING, related_name="team4")
    score4 = models.IntegerField(default=0)
    start_time = models.DateTimeField('date published')
    finished = models.BooleanField(default=False)
    special_name = models.CharField(max_length=25,default = "")