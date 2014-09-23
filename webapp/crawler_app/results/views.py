from django.views.generic import ListView

from results.models import CrawlerResult


class CrawlerResultList(ListView):
    model = CrawlerResult
