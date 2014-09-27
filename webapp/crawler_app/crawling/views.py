import os
import subprocess

from django.http import HttpResponse, Http404
from django.views.generic import ListView

from crawler_app.settings import SCRAPY_DIR, CRAWLERS
from crawling.models import CrawlerResult


class CrawlerResultList(ListView):
    queryset = CrawlerResult.objects.all().order_by('-time_posted')
    template_name = 'crawling/crawlerresult_list.html'


def crawl_all_sources(request):
    for crawler in CRAWLERS:
        crawl_source(request, crawler)

    return HttpResponse('Done')


def crawl_source(request, source):
    if source not in CRAWLERS:
        raise Http404

    os.chdir(SCRAPY_DIR)
    subprocess.call(['scrapy', 'crawl', source])
    return HttpResponse('Done')
