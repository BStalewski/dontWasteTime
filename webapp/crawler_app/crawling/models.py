from django.db import models


class CrawlerResult(models.Model):
    NEW = u'NEW'
    ACC = u'ACC'
    IGN = u'IGN'

    CRAWLING_STATUSES = (
        (NEW, u'new'),
        (ACC, u'accepted'),
        (IGN, u'ignored'),
    )

    title = models.CharField(max_length=200)
    link = models.URLField()
    desc = models.TextField()
    price = models.IntegerField()
    time_posted = models.DateTimeField()
    source = models.CharField(max_length=50, default='')
    status = models.CharField(max_length=5, choices=CRAWLING_STATUSES, default=NEW)

    def is_acceptable(self):
        return self.status != CrawlerResult.ACC

    def is_ignorable(self):
        return self.status != CrawlerResult.IGN
