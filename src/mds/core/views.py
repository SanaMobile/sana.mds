'''
Created on Aug 3, 2012

@author: Sana Development
'''
import cjson
import logging

from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms.models import modelformset_factory
from .forms import *

from django.shortcuts import render_to_response,redirect
from django.template import RequestContext 

from mds.api import version
from mds.api.responses import JSONResponse
from mds.api.v1.v2compatlib import sort_by_node
from .models import Event

def home(request):
    """Top level url
    
    Displays ::
        {"path": HttpRequest.path, 
         "host": HttpRequest.get_host(), 
         "version": mds.api.version, 
         "service": "REST"}
    """
    username = request.REQUEST.get('username', 'empty')
    password = request.REQUEST.get('password','empty')
    user = authenticate(username=username, password=password)
    if user is not None:
        return HttpResponse(cjson.encode( {
               'status':'SUCCESS',
               'code':200,
               'message': version()}))
    else:
        message = unicode('UNAUTHORIZED:Invalid credentials!')
        logging.warn(message)
        logging.debug(u'User' + username)
        return HttpResponse(cjson.encode({
                'status':'FAIL',
                'code':401, 
                'message': message}))
    

def _list(request,*args,**kwargs):
    query = dict(request.GET.items())
    start = int(query.get('start', 1))
    limit = int(query.get('limit', 20))
    objects = Event.objects.all().filter().order_by('-created')
    paginator = Paginator(objects, limit, allow_empty_first_page=True)
    objs = []
    for p in paginator.page(start).object_list.all():
        obj = p.to_python()
        m = obj.pop('message')
        try:
            obj['message'] = cjson.decode(m,True)
        except:
            obj['message'] = m
        objs.append(obj)
    data = {'objects': objs,
            'limit': limit,
            'start': start,
            "rate": int(query.get('refresh', 5)),
            'range': range(1, paginator.num_pages + 1),
            "version": settings.API_VERSION }
    return data

def log_index(request,*args,**kwargs):
    data = _list(request)
    return render_to_response('logging/index.html', RequestContext(request,data))

def log_list(request):
    data = _list(request)
    return render_to_response('logging/list.html', RequestContext(request,data))

def log_report(request):
    post = dict(request.POST.items())
    selected = []
    for k,v in post.items():
        if v:
            selected.append(k)
    objects = Event.objects.all().filter(uuid__in=selected)
    return JSONResponse(objects)

def log_detail(request, uuid):
    log = Event.objects.get(uuid=uuid)
    data = []
    messages = cjson.decode(log.messages)
    for m in messages:
        try:
            m['message'] = cjson.decode(m['message'])
        except:
            pass
        
        data.append(m)
#           m['message']  = cjson.decode(m['message'])
#            data.append(m)
#        except:
            
            
    message = { 'message': data, 'uuid': uuid, }
    return HttpResponse(cjson.encode(message))

def log(request,*args,**kwargs):
    query = dict(request.GET.items())
    page = int(query.get('page', 1))
    page_size = int(query.get('page_size', 20))
    
    data = {'object_list': {},
            'page_range': range(0, 1),
            'page_size': page_size,
            'page': page,
            "rate": int(query.get('refresh', 5)) }
    return render_to_response('logging/index.html', RequestContext(request,data))

@login_required(login_url='/mds/login/')
def encounter(request,**kwargs):
    tmpl = 'core/mobile/encounter.html'
    uuid = kwargs.get('uuid',None) if kwargs else None
    if kwargs:
        tmpl = 'core/mobile/encounter.html'
        encounters = Encounter.objects.filter(**kwargs)
        num = encounters.count()
        data = []
        
        for encounter in encounters:
            obj = { 'procedure' : encounter.procedure,
                 'subject' : encounter.subject,
                 'device' : encounter.device,
                 'observer' :encounter.observer }
            obsqs = Observation.objects.filter(encounter=encounter.uuid)
            observations = []
            for obs in sort_by_node(obsqs,descending=False):
                obsdata = { "node": obs.node,
                        "concept": obs.concept.name}
                if obs.concept.is_complex:
                    obsdata["url"] = obs.value_complex.url
                    obsdata["thumb"] = u''
                    obsdata["value"] =  obs.value_complex.url
                else:
                    obsdata["url"] = ""
                    obsdata["value"] =  unicode(obs.value)
                observations.append(obsdata)
            obj['observations'] = observations
            data.append(obj)
        
        #data = encounters
    else:
        tmpl = 'core/mobile/encounter_list.html'
        data = Encounter.objects.all()
        num = data.count()
    return render_to_response(tmpl, 
                              context_instance=RequestContext(request,{ "objs": data , 'count': num }))

def subject(request,**kwargs):
    #if not request.user.is_authenticated():
    #    return render_to_response('core/login.html')
    uuid = kwargs.get('uuid',None) if kwargs else None
    if uuid:
        tmpl = 'core/mobile/subject.html'
        subjects = Subject.objects.filter(uuid=uuid)
    else:
        tmpl = 'core/mobile/subject_list.html'
        subjects = Subject.objects.all()
    return render_to_response(tmpl, 
                               context_instance=RequestContext(request,{ "objs": subjects }))

def subject_create(request,**kwargs):
    return render_to_response('core/mobile/registration.html', 
                               context_instance=RequestContext(request,{}))
                               
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
        
    return render_to_response(tmpl,
                                context_instance=RequestContext(request, 
                                                                {'subject_form':  SurgicalSubjectForm(),
                                                                 'encounter_form': SurgicalIntakeForm(),
                                                                 'sa_form' : SurgicalAdvocateFollowUpForm(),
                                                                 'observer': observer}))

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
        
    return render_to_response(tmpl,
                                context_instance=RequestContext(request, 
                                                                {'subject_form':  SurgicalSubjectForm(),
                                                                 'encounter_form': SurgicalIntakeForm(),
                                                                 'sa_form' : SurgicalAdvocateFollowUpForm(),
                                                                 'observer': observer}))
def index_page(request,**kwargs):
    flavor = request.GET.get('flavor',None)
    tmpl = 'core/index.html'
    if flavor:
        if flavor == 'mobile':
            tmpl = 'core/mobile/index.html'
        else:
            tmpl = 'core/index.html'
        
    return render_to_response(tmpl,
                                context_instance=RequestContext(request, {'flavor': flavor}))

def mobile_authenticate(request,**kwargs):
    username = request.REQUEST.get('username', 'empty')
    password = request.REQUEST.get('password','empty')
    user = authenticate(username=username, password=password)
    observer = None
    role = 0
    try:
        observer = Observer.objects.get(user__username=username)
        role = 1 if user.is_superuser else 2
    except:
        pass
    if user is not None and observer is not None:
        return HttpResponse(cjson.encode( {
               'status':'SUCCESS',
               'code':200,
               'message': [
                    {
                        "uuid": observer.uuid,
                        "role": role,
                    }
                ]}))
    else:
        message = unicode('UNAUTHORIZED:Invalid credentials!')
        logging.warn(message)
        logging.debug(u'User' + username)
        return HttpResponse(cjson.encode({
                'status':'FAIL',
                'code':401, 
                'message': []}))

@login_required(login_url='/mds/login/')
def encounter_task(request, **kwargs):
    form = EncounterTaskForm()
    return render_to_response("core/etask.html", 
                              context_instance=RequestContext( request, 
                                {
                                 'form':form,
                                 'flavor': flavor
                                })
                             )
if __name__ == 'main':
    data = {"data": [
               {'line_number': 44, 
                'level_number': 10, 
                'delta': '0.000s', 
                'timestamp': 1344815434.9979069, 
                'level_name': 'DEBUG', 
                'function_name': 'execute', 
                'message': u'(0.002) SELECT \"core_concept\".\"id\", \"core_concept\".\"uuid\", \"core_concept\".\"created\", \"core_concept\".\"modified\", \"core_concept\".\"name\", \"core_concept\".\"display_name\", \"core_concept\".\"description\", \"core_concept\".\"conceptclass\", \"core_concept\".\"datatype\", \"core_concept\".\"mimetype\", \"core_concept\".\"constraint\" FROM \"core_concept\"; args=()', 
                'module': 'util', 
                'filename': 'util.py'}], 
            "id": "2bbeb878-33f1-4590-9237-e41b151fa553"}