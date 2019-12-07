from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField(blank=True)
    author = models.CharField(max_length=50)

    class Meta:
        abstract = True

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
