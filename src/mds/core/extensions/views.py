'''SSI pilot specific views

@author: Sana Development
'''
import cjson
import logging

from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core import serializers
from django.http import HttpResponse
from django.forms.models import modelformset_factory
from .forms import *

from django.shortcuts import render_to_response,redirect
from django.template import RequestContext 

from mds.api import version
from mds.api.responses import JSONResponse
from mds.api.v1.v2compatlib import sort_by_node
from mds.core.models import *
from mds.core.forms import *

__all__ = [
    'intake',
]

@login_required(login_url='/mds/login')
def intake(request,**kwargs):
    method = request.META['REQUEST_METHOD']
    if method == 'POST':
        return intake_post(request,kwargs=kwargs)
    else:
        return intake_get(request,kwargskwargs=kwargs)

def intake_post(request,**kwargs):    
    user = request.user
    observer = Observer.objects.get(user=request.user)
    flavor = request.GET.get('flavor',None)
    tmpl = 'core/intake.html'
    if flavor:
        if flavor == 'mobile':
            tmpl = 'core/mobile/intake.html'
        else:
            tmpl = 'core/intake.html'
        
    return render_to_response(
        tmpl,
        context_instance=RequestContext(
            request, 
            {'subject_form':  SurgicalSubjectForm(),
             'encounter_form': SurgicalIntakeForm(),
             'sa_form' : SurgicalAdvocateFollowUpForm(),
             'observer': observer}
        ))

def intake_get(request,**kwargs):
    # Get the user
    user = request.user
    observer = Observer.objects.get(user=request.user)
    flavor = request.GET.get('flavor',None)
    tmpl = 'core/intake.html'
    if flavor:
        if flavor == 'mobile':
            tmpl = 'core/mobile/intake.html'
        else:
            tmpl = 'core/intake.html'
        
    return render_to_response(
        tmpl,
        context_instance=RequestContext(
            request, 
            {'subject_form':  SurgicalSubjectForm(),
             'encounter_form': SurgicalIntakeForm(),
             'sa_form' : SurgicalAdvocateFollowUpForm(),
             'observer': observer}
             ))
