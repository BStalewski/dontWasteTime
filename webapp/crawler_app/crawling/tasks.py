from celery import shared_task

from crawling.utils import crawl, crawl_all


@shared_task
def update_crawled_results():
    crawl_all()


@shared_task
def update_crawled_results_for(source):
    crawl(source)
