from django.conf.urls import patterns, url
from .views import *
__all__ = [
    'urlpatterns',
]
urlpatterns = patterns(    
    '',
   url(r'^surgicalsubject/$', SurgicalSubjectListView.as_view(),name='surgicalsubject-list'),
    url(r'^surgicalsubject/new/$', SurgicalSubjectCreateView.as_view(),name='surgicalsubject-create'),
    url(r'^surgicalsubject/(?P<pk>[^/]+)/$', SurgicalSubjectUpdateView.as_view(),name='surgicalsubject-edit'),
    url(r'^subjectsubject/(?P<pk>\d+)/detail/$', SurgicalSubjectDetailView.as_view(), name='surgicalsubject-detail'),
)
