from django.db import models


class CrawlItem(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()
    desc = models.TextField()
    price = models.IntegerField()
    time_posted = models.DateTimeField()
