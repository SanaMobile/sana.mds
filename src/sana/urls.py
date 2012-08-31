"""The Django url to handler mappings for mDS.


:Authors: Sana dev team
:Version: 2.0
"""

from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.views.generic.simple import redirect_to

from django.contrib import admin

from sana.api.v1.v2compatlib import redirect_to_v1

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'sana.core.views.home', name="home"),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': settings.MEDIA_ROOT }),
    url(r'^core/', include('sana.core.urls', namespace='core')),
    url(r'^mds/', include('sana.mds.urls', namespace='mds')),
    url(r'^mrs/', include('sana.mrs.urls', namespace='mrs')),
    # ADMIN
    (r'^admin/', include(admin.site.urls)),
)


"""The mappings Django uses to send requests to the appropriate handlers."""

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
    
v1patterns = patterns(
    '',
    
    url(r'^notifications/$',
        redirect_to,
        {'url': '/mrs/notifications/'},
        name="sana-list-notifications-redirect"),

    url(r'^notifications/submit/$',
        redirect_to,
        {'url': '/mrs/notifications/submit/'},
        name="sana-api-notification-submit-redirect"),

    url(r'^notifications/submit/email/$',
        redirect_to,
        {'url': '/mrs/notifications/submit/email/'},
        name="sana-api-email-notification-submit-redirect"),

     url(r'^json/patient/list/$',
        redirect_to,
        {'url': '/mrs/json/patient/list/'},
         name="sana-json-patient-list-redirect"),

     url(r'^json/patient/(?P<id>[0-9-]+)/$',
        redirect_to,
        {'url': '/mrs/json/patient/(?P<id>[0-9-]+)/'},
         name="sana-json-patient-get-redirect"),


    url(r'^json/validate/credentials/$',
        redirect_to,
        {'url': '/mrs/json/validate/credentials/',},
        name = "sana-json-validate-credentials-redirect"),

    url(r'^procedure/submit/$',
        redirect_to,
        {'url': '/mrs/json/validate/credentials/'},
        name="sana-html-procedure-submit-redirect"),

    url(r'^json/procedure/submit/$',
        redirect_to,
        {'url': ''},
        name="sana-json-procedure-submit-redirect"),

    url(r'^json/binary/submit/$',
        redirect_to,
        {'url': '/mrs/json/binary/submit/'},
        name="sana-json-binary-submit-redirect"),

    url(r'^json/binarychunk/submit/$',
        redirect_to,
        {'url': '/mrs/json/binarychunk/submit/'},
        name="sana-json-binarychunk-submit-redirect"),

    url(r'^json/textchunk/submit/$',
        redirect_to,
        {'url': '/mrs/json/textchunk/submit/'},
        name="sana-json-binarychunk-hack-submit-redirect"),

    url(r'^json/eventlog/submit/$',
        redirect_to,
        {'url': '/mrs/json/eventlog/submit/'},
        name="sana-json-eventlog-submit-redirect"),
)

_compats = {'v1': v1patterns }

if settings.COMPAT_URLS:
    for compat in settings.COMPAT_URLS:
        urlpatterns += _compats[compat]
        
    