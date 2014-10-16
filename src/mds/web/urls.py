"""The Django url to handler mappings.


:Authors: Sana dev team
:Version: 2.0
"""
from django.conf.urls import patterns, url, include

urlpatterns = patterns(    
    #'mds.web',
    '',
    url(r'^$',
        'mds.web.views.web_root',
        name="portal"),
    #url(r'^login/$', 'django.contrib.auth.views.login'),
    #url(r'^mobile/authenticate/$', 'views.mobile_authenticate', name='mobile-authenticate'),
    url(r'^etask/$', 'mds.web.views.encounter_task', name='encounter-task'),
    url(r'^etask/list/$', 'mds.web.views.task_list', name='encounter-task-list'),
    url(r'^etask/(?P<uuid>[^/]+)/$', 'mds.web.views.edit_encounter_task', name='edit-encounter-task'),
    url(r'^registration/$', 'mds.web.views.registration', name='register-patient'),
    url(r'^encounter/$', 'mds.web.views.web_encounter', name='encounter'),

    url(r'^logs/$', 'mds.web.views.logs', name='log-index'),
    url(r'^logs/list/$', 'mds.web.views.log_list', name='log-list'),

)