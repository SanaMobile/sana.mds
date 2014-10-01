"""The Django url to handler mappings.


:Authors: Sana dev team
:Version: 2.0
"""
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns(    
    'web',
    url(r'^$',
        'views.web_root',
        name="portal"),
    #url(r'^login/$', 'django.contrib.auth.views.login'),
    #url(r'^mobile/authenticate/$', 'views.mobile_authenticate', name='mobile-authenticate'),
    url(r'^etask/$', 'views.encounter_task', name='encounter-task'),
    url(r'^etask/list/$', 'views.task_list', name='encounter-task-list'),
    url(r'^etask/(?P<uuid>[^/]+)/$', 'views.edit_encounter_task', name='edit-encounter-task'),
    url(r'^registration/$', 'views.registration', name='register-patient'),
    url(r'^encounter/$', 'views.web_encounter', name='encounter'),

    url(r'^logs/$', 'views.logs', name='log-index'),
    url(r'^logs/list/$', 'views.log_list', name='log-list'),

)