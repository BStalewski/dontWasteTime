import os
import subprocess

from django.http import HttpResponse
from django.views.generic import ListView
from crawler_app.settings import SCRAPY_DIR

from crawling.models import CrawlerResult


class CrawlerResultList(ListView):
    queryset = CrawlerResult.objects.all().order_by('-time_posted')
    template_name = 'crawling/crawlerresult_list.html'


def new_crawling(request):
    os.chdir(SCRAPY_DIR)
    subprocess.call(['scrapy', 'crawl', 'gumtree'])
    return HttpResponse('Done')
