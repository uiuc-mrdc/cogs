from djongo import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField(blank=True)
    author = models.CharField(max_length=50)

    class Meta:
        abstract = True

class Entry(models.Model):
    blog = models.EmbeddedModelField(
        model_container=Blog,
    )

    headline = models.CharField(max_length=255)
    objects = models.DjongoManager()
    
    
class Teams(models.Model):
    teamName = models.CharField(max_length=100)
    schoolName = models.CharField(max_length=200)
    def __str__(self):
        return self.teamName

class ScoringOptions(models.Model):
    actionName = models.CharField(max_length=40)
    Limit = models.IntegerField(default=0)
    Value = models.IntegerField()
    extraData = models.CharField(max_length=20)
    InputGroup = models.CharField(max_length=20)
    def __str__(self):
        return self.actionName

class LiveScoring(models.Model):
    actionID = models.ForeignKey(ScoringOptions, on_delete=models.DO_NOTHING)
    time = models.DateTimeField('date published')
    teamID = models.ForeignKey(Teams, on_delete=models.DO_NOTHING)
    def __str__(self):
        return ", ".join([str(self.actionID),str(self.teamID)])
