from django.conf import settings
from django.conf.urls import patterns, url, include
#from django.views.generic.simple import redirect_to

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'clients.views.version', name="android"),
    url(r'^download/$', 'mds.clients.views.download_current', name="download-current"),
    url(r'^download/(?P<version>\w+)/$', 'mds.clients.views.download_version', name="download-version"),
    )
