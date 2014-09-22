# -*- coding: utf-8 -*-

from scrapy.contrib.djangoitem import DjangoItem
from results.models import CrawlerResult


class CrawlerItem(DjangoItem):
    django_model = CrawlerResult
