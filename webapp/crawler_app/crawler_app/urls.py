from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login

urlpatterns = patterns(
    '',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout_then_login),
    url(r'^crawling/', include('crawling.urls')),
    url(r'^$', 'crawling.views.empty_url'),
)
