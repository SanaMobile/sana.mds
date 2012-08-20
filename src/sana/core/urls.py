"""The Django url to handler mappings.


:Authors: Sana dev team
:Version: 2.0
"""
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from piston.resource import Resource

from sana.core.handlers import *

concept_handler = Resource(ConceptHandler)
relationship_handler = Resource(RelationshipHandler)
relationshipcategory_handler = Resource(RelationshipCategoryHandler)
device_handler = Resource(DeviceHandler)
encounter_handler = Resource(EncounterHandler)
notification_handler = Resource(NotificationHandler)
observation_handler = Resource(ObservationHandler)
observer_handler = Resource(ObserverHandler)
procedure_handler = Resource(ProcedureHandler)
subject_handler = Resource(SubjectHandler)
requestlog_handler = Resource(RequestLogHandler)
restapi_handler = Resource(DocHandler)


# non-restful urls
urlpatterns = patterns(    
    'core',
    url(r'^$',
        'views.home',
        name="home"),
    
    url(r'^logs/$', 'views.log_index', name='log-index'),
    url(r'^logs/list/$', 'views.log_list', name='log-list'),
    url(r'^logs/detail/(?P<uuid>[^/]+)/$', 'views.log_detail', name='log-detail'),
                                          
    # docs
    url(r'^docs/$', restapi_handler, name='core-docs'),     
              
)    

extra_patterns = patterns(
    '',
    
    # notification
    url(r'^notification/$', notification_handler, name='notification-list'),
    url(r'^notification/(?P<uuid>[^/]+)/$', notification_handler, name='notification'),
    
    # request logs   
    url(r'^requestlog/$', requestlog_handler, name='requestlog-list'),
    url(r'^requestlog/(?P<uuid>[^/]+)/$', requestlog_handler, name='requestlog'),
    
    # concepts
    url(r'^concept/$', concept_handler, name='concept-list'),
    url(r'^concept/(?P<uuid>[^/]+)/$', concept_handler, name='concept'),
    url(r'^concept/(?P<uuid>[^/]+)/relationship/$', concept_handler, name='concept-relationship', kwargs={'related':'relationship'}),
    url(r'^concept/(?P<uuid>[^/]+)/procedure/$', concept_handler, name='concept-procedure', kwargs={'related':'procedure'}),
    
    # concept relationships
    url(r'^relationship/$', relationship_handler,name='relationship-list'),
    url(r'^relationship/(?P<uuid>[^/]+)/$', relationship_handler,name='relationship'),
    
    # concept relationship categories
    url(r'^relationshipcategory/$', relationshipcategory_handler,
        name='relationshipcategory-list'),
    url(r'^relationshipcategory/(?P<uuid>[^/]+)/$', relationshipcategory_handler,
        name='relationshipcategory'),
    
    # devices
    url(r'^device/$', device_handler, name='device-list'),
    url(r'^device/(?P<uuid>[^/]+)/$', device_handler, name='device'),
    
    # encounters
    url(r'^encounter/$', encounter_handler, name='encounter-list'),
    url(r'^encounter/(?P<uuid>[^/]+)/$', encounter_handler, name='encounter'),
    
    # observations
    url(r'^observation/$', observation_handler, name='observation-list'),
    url(r'^observation/(?P<uuid>[^/]+)/$', observation_handler, name='observation'),
    
    # observers
    url(r'^observer/$', observation_handler, name='observer-list'),
    url(r'^observer/(?P<uuid>[^/]+)/$', observer_handler, name='observer'),
    
    # procedures
    url(r'^procedure/$', procedure_handler, name='procedure-list'),
    url(r'^procedure/(?P<uuid>[^/]+)/$', procedure_handler, name='procedure'),
    
    # subjects
    url(r'^subject/$', subject_handler, name='subject-list'),
    url(r'^subject/(?P<uuid>[^/]+)/$', subject_handler, name='subject'),
)

# add the non-RESTful urls
urlpatterns += extra_patterns

