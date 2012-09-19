"""The Django url to handler mappings.


:Authors: Sana dev team
:Version: 2.0
"""
from django.conf.urls.defaults import patterns, url, include
from piston.resource import Resource

from .handlers import *

concept_handler = Resource(ConceptHandler)
relationship_handler = Resource(RelationshipHandler)
relationshipcategory_handler = Resource(RelationshipCategoryHandler)
device_handler = Resource(DeviceHandler)
encounter_handler = Resource(EncounterHandler)
event_handler = Resource(EventHandler)
notification_handler = Resource(NotificationHandler)
observation_handler = Resource(ObservationHandler)
observer_handler = Resource(ObserverHandler)
procedure_handler = Resource(ProcedureHandler)
session_handler = Resource(SessionHandler)
subject_handler = Resource(SubjectHandler)

doc_handler = Resource(DocHandler)

# non-restful urls
urlpatterns = patterns(    
    'core',
    url(r'^$',
        'views.home',
        name="home"),
    
    # Web views of logs
    url(r'^logs/$', 'views.log_index', name='log-index'),
    url(r'^logs/list/$', 'views.log_list', name='log-list'),
    url(r'^logs/detail/(?P<uuid>[^/]+)/$', 'views.log_detail', name='log-detail'),
                                          
    # docs
    url(r'^docs/$', doc_handler, name='core-docs'),     
              
)    

extra_patterns = patterns(
    '',
    # session auth
    url(r'^session/$', session_handler, name='session-list'),
    
    # notification
    url(r'^notification/$', notification_handler, name='notification-list'),
    url(r'^notification/(?P<uuid>[^/]+)/$', notification_handler, name='notification'),
    
    # events   
    url(r'^event/$', event_handler, name='event-list'),
    url(r'^event/(?P<uuid>[^/]+)/$', event_handler, name='event'),
    
    # concepts
    url(r'^concept/$', concept_handler, name='concept-list'),
    url(r'^concept/(?P<uuid>[^/]+)/$', concept_handler, name='concept'),
    url(r'^concept/(?P<uuid>[^/]+)/relationship/$', concept_handler, name='concept-relationships', kwargs={'related':'relationship'}),
    url(r'^concept/(?P<uuid>[^/]+)/procedure/$', concept_handler, name='concept-procedures', kwargs={'related':'procedure'}),
    
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
    url(r'^encounter/(?P<uuid>[^/]+)/observation/$', encounter_handler, name='encounter-observations', kwargs={'related':'observation'}),
    
    # observations
    url(r'^observation/$', observation_handler, name='observation-list'),
    url(r'^observation/(?P<uuid>[^/]+)/$', observation_handler, name='observation'),
    
    # observers
    url(r'^observer/$', observer_handler, name='observer-list'),
    url(r'^observer/(?P<uuid>[^/]+)/$', observer_handler, name='observer'),
    
    # procedures
    url(r'^procedure/$', procedure_handler, name='procedure-list'),
    url(r'^procedure/(?P<uuid>[^/]+)/$', procedure_handler, name='procedure'),
    
    # subjects
    url(r'^subject/$', subject_handler, name='subject-list'),
    url(r'^subject/(?P<uuid>[^/]+)/$', subject_handler, name='subject'),
    url(r'^subject/(?P<uuid>[^/]+)/encounter/$', subject_handler, name='subject-encounters', kwargs={'related':'procedure'}),
)

# add the non-RESTful urls
urlpatterns += extra_patterns

