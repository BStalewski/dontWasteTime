from django.http import HttpResponse, Http404
from django.views.generic import ListView

from crawler_app.settings import CRAWLERS
from crawling.models import CrawlerResult
from crawling.tasks import update_crawled_results, update_crawled_results_for


class CrawlerResultList(ListView):
    queryset = CrawlerResult.objects.all().order_by('-time_posted')
    template_name = 'crawling/crawlerresult_list.html'


def crawl_all_sources(request):
    update_crawled_results.delay()

    return HttpResponse('Done')


def crawl_source(request, source):
    if source not in CRAWLERS:
        raise Http404

    update_crawled_results_for.delay(source)

    return HttpResponse('Done')
