from django.conf.urls import patterns, url

from crawling.views import CrawlerResultList, new_crawling

urlpatterns = patterns(
    '',

    url(r'^results$', CrawlerResultList.as_view()),
    url(r'^new$', new_crawling),
)
