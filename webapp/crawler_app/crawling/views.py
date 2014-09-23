from django.views.generic import ListView

from crawling.models import CrawlerResult


class CrawlerResultList(ListView):
    model = CrawlerResult
