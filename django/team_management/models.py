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
    action_id = models.ForeignKey(ScoringType, on_delete=models.DO_NOTHING)
    time = models.DateTimeField('date published')
    team_id = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    def __str__(self):
        return ", ".join([str(self.action_id),str(self.team_id)])
