from django.conf.urls import patterns, url

from results.views import CrawlerResultList

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'crawler_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', CrawlerResultList.as_view()),
)
