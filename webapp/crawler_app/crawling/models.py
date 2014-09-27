from django.db import models


class CrawlerResult(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()
    desc = models.TextField()
    price = models.IntegerField()
    time_posted = models.DateTimeField()
    source = models.CharField(max_length=50, default='')
