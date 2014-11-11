from django.conf.urls import patterns, url

import crawling.views as crv

urlpatterns = patterns(
    '',

    url(r'^results$', crv.CrawlerResultList.as_view()),
    url(r'^new$', crv.CrawlerNewList.as_view()),
    url(r'^accepted$', crv.CrawlerAcceptedList.as_view()),
    url(r'^ignored$', crv.CrawlerIgnoredList.as_view()),

    url(r'^crawl/$', crv.crawl_all_sources),
    url(r'^crawl/(?P<source>\w+)/$', crv.crawl_source),

    url(r'^accept/(?P<id>\d+)/$', crv.accept),
    url(r'^ignore/(?P<id>\d+)/$', crv.ignore),
)
