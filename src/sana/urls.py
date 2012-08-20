"""The Django url to handler mappings for mDS.


:Authors: Sana dev team
:Version: 2.0
"""
import sys

from django.conf import settings
from django.conf.urls.defaults import patterns, url, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'sana.core.views.home', name="home"),
    url(r'^core/', include('sana.core.urls', namespace='core')),
    url(r'^mds/', include('sana.mds.urls', namespace='mds')),
    # ADMIN
    (r'^admin/', include(admin.site.urls)),
)


"""The mappings Django uses to send requests to the appropriate handlers."""

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )