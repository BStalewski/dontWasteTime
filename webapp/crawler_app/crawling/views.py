from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from crawler_app.settings import CRAWLERS
from crawling.models import CrawlerResult
from crawling.tasks import update_crawled_results, update_crawled_results_for


class CrawlerResultList(ListView):
    queryset = CrawlerResult.objects.all().order_by('-time_posted')
    template_name = 'crawling/crawlerresult_list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CrawlerResultList, self).dispatch(*args, **kwargs)


class CrawlerNewList(CrawlerResultList):
    queryset = CrawlerResult.objects.filter(status=CrawlerResult.NEW).order_by('-time_posted')
    template_name = 'crawling/crawler_new_list.html'


class CrawlerAcceptedList(CrawlerResultList):
    queryset = CrawlerResult.objects.filter(status=CrawlerResult.ACC).order_by('-time_posted')
    template_name = 'crawling/crawler_acc_list.html'


class CrawlerIgnoredList(CrawlerResultList):
    queryset = CrawlerResult.objects.filter(status=CrawlerResult.IGN).order_by('-time_posted')
    template_name = 'crawling/crawler_ign_list.html'


def crawl_all_sources(request):
    update_crawled_results.delay()

    return HttpResponse('Done')


def crawl_source(request, source):
    if source not in CRAWLERS:
        raise Http404

    update_crawled_results_for.delay(source)

    return HttpResponse('Done')


@transaction.atomic
@csrf_exempt
def accept(request, id):
    update_status(id, CrawlerResult.ACC)
    return HttpResponse('Done')


@transaction.atomic
@csrf_exempt
def ignore(request, id):
    update_status(id, CrawlerResult.IGN)
    return HttpResponse('Done')


def update_status(id, status):
    crawling = CrawlerResult.objects.select_for_update().get(id=id)
    crawling.status = status
    crawling.save()
