from django.conf.urls import patterns, url

from crawling.views import CrawlerResultList, crawl_all_sources, crawl_source

urlpatterns = patterns(
    '',

    url(r'^results$', CrawlerResultList.as_view()),
    url(r'^new/$', crawl_all_sources),
    url(r'^new/(?P<source>\w+)/$', crawl_source),
)
