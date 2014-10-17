import cjson
import logging

from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django import forms
from django.forms.models import modelformset_factory

from django.shortcuts import render_to_response,redirect
from django.template import RequestContext 
from django.views.generic import DetailView, ListView

from mds.api import version
from mds.api.responses import JSONResponse
from mds.core.models import *
from .forms import *
from mds.tasks.models import *

#__all__ = ['home', 'index','intake']

def home(request):
    """Top level url
    
    Displays ::
        {"status": "SUCCESS | FAIL", 
         "code",  "200|401",
         "message": mds.api.version() }
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

class _metadata(object):
    def __init__(self,request):
        self.params = request.COOKIES
        self.flavor = self.params.get("flavor",None)
        self.debug = []
        self.errors = []
        self.mode = self.params.get("mode","normal")
        if self.mode == "verbose":
            self.debug.append("mode: %s" % self.mode)
            for k,v in request.session.items():
                self.debug.append("%s : %s" %(k,v))
        else:
            self.debug.append("Nothing to see here.")

    @property
    def messages(self):
            return self.debug

@login_required(login_url='/login/')
def web_root(request, **kwargs):
    metadata = _metadata(request)
    return render_to_response("web/index.html", 
                              context_instance=RequestContext(request,{
                              'flavor': metadata.flavor,
                              'errors': metadata.errors,
                              'messages' : metadata.messages
                            }))

def registration(request, **kwargs):
    metadata = _metadata(request)
    return render_to_response("web/registration.html", 
                              context_instance=RequestContext(request,{
                              'form':  SurgicalSubjectForm(),
                              'flavor': metadata.flavor,
                              'errors': metadata.errors,
                              'messages' : metadata.messages
                               }))

@login_required(login_url='/mds/login/')
def encounter_task(request, **kwargs):
    flavor = kwargs.get('flavor',None) if kwargs else None
    params = request.COOKIES
    data = {}
    debug = []
    errors = []

    tmpl = "web/etask.html"
    # Get the request cookies and check for values to preload
    mode = params.get("mode","normal")
    debug.append(u'mode: %s' % mode)
    # Should use this to track IP's?
    device = params.get('device', None)
    if device:
        device = Device.objects.get(uuid=device)
    data['device'] = device
    # Check for a preassigned subject
    subject = params.get('subject', None)
    new_patient = bool(params.get("new_patient", False))
    if subject:
        subject = Subject.objects.get(uuid=subject)
        
    else:
        if mode and mode == "test":
            subject = Subject.objects.get(uuid="e7d4bdd8-2cfa-400c-b4bc-330fcd2497fc")
    data["subject"] = subject
    
    form = EncounterTaskForm(initial=data)
    return render_to_response(tmpl, 
                              context_instance=RequestContext( request, 
                                {
                                 'form':form,
                                 'flavor': flavor,
                                 'errors': errors,
                                 'debug' : debug
                                })
                             )
# TODO make this better
# Procedure UUid tp form mappings
_procedure_forms = {
    "303a113c-6345-413f-88cb-aa6c4be3a07d": IntakeForm,
}

@login_required(login_url='/mds/login/')
def edit_encounter_task(request, uuid, **kwargs):
    if(uuid):
        try:
            task = EncounterTask.objects.get(uuid=uuid)
        except:
            return encounter_task(request)
    flavor = kwargs.get('flavor',None) if kwargs else None
    params = request.COOKIES
    data = {}
    debug = []
    errors = []

    tmpl = "web/etask.html"
    # Get the request cookies and check for values to preload
    mode = params.get("mode","normal")
    debug.append(u'mode: %s' % mode)
    # Should use this to track IP's?
    device = params.get('device', None)
    if device:
        device = Device.objects.get(uuid=device)
    data['device'] = device
    task = None
    # Check for a preassigned subject

    
    form = EncounterTaskForm(task)
    return render_to_response(tmpl, 
                              context_instance=RequestContext( request, 
                                {
                                 'form':form,
                                 'flavor': flavor,
                                 'errors': errors,
                                 'debug' : debug
                                })
                             )
@login_required(login_url='/mds/login/')
def web_encounter(request, **kwargs):
    _cookies = request.COOKIES
    params = request.COOKIES
    data = {}
    errors = []
    debug = []

    form_klazz = EmptyEncounterForm

    # Get the request cookies and check for values to preload
    mode = params.get("mode","normal")

    # Allow the flavor to be sent as kw or cookie
    flavor = kwargs.get('flavor',None) if kwargs else None
    if not flavor:
        flavor = _cookies.get("flavor",None)

    # Should use this to track IP's?
    device = params.get('device', "2fc0a9f7-384b-4d97-8c1c-aa08f0e12105")
    if device:
        device = Device.objects.get(uuid=device)
    data["device"] = device

    # Defaults to generic encounter
    concept = params.get('concept', "521b0825-14c9-49e5-a95e-462a01e2ae05")
    if concept:
        concept = Concept.objects.get(uuid=concept)
    data["concept"] = concept

    # Defaults to Intake procedure for now
    # TODO move to setting?
    procedure = params.get('procedure', "303a113c-6345-413f-88cb-aa6c4be3a07d")
    if procedure:
        procedure = Procedure.objects.get(uuid=procedure)
    data["procedure"] = procedure

    # Check for a preassigned subject
    subject = params.get('subject', None)
    if subject:
        subject = Subject.objects.get(uuid=subject)
    else:
        if mode and mode == "test":
            subject = Subject.objects.get(uuid="e7d4bdd8-2cfa-400c-b4bc-330fcd2497fc")
    data["subject"] = subject

    # Check that we have an observer
    observer = Observer.objects.get(user__username=request.user)
    data['observer'] = observer

    form_klazz = _procedure_forms.get(procedure.uuid, EmptyEncounterForm) if procedure else form_klazz
    try:
        form = form_klazz(initial=data)
        if mode == "verbose":
            debug.append("Initial data:")
            for k,v in data.items():
                debug.append(u"  %s : %s" % (k,v))
        else:
            debug.append("Nothing to see here")
            for k,v in data.items():
                debug.append(u"  %s : %s" % (k,v))
    except:
        form = form_klazz()
        errors.append(u"Problem with initializing form with data")
        errors.append(u"%s" % form_klazz)
        for k,v in data.items():
            errors.append(u"%s : %s" % (k,v))

    return render_to_response("web/encounter_form.html", 
                              context_instance=RequestContext( request, 
                                {
                                 'form': form,
                                 'flavor': flavor,
                                 'errors': errors,
                                 'messages' : debug,
                                 'debug' : debug
                                })
                             )

@login_required(login_url='/mds/login/')
def task_list(request):
    query = dict(request.GET.items())
    page = int(query.get('page', 1))
    page_size = int(query.get('page_size', 20))
    prange =  range(0, 1)

    task_list = EncounterTask.objects.all()
    paginator = Paginator(task_list, page_size)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        tasks = paginator.page(page)
    except (EmptyPage, InvalidPage):
        tasks = paginator.page(paginator.num_pages)
    prange = range(1,paginator.num_pages)
    return render_to_response("web/etask_list.html", 
                              context_instance=RequestContext( request, 
                                {
                                 'tasks':tasks.object_list,
                                 'range':prange,
                                 'page': page,
                                }
                              )
    )

def _list(request,*args,**kwargs):
    query = dict(request.GET.items())
    start = int(query.pop('start', 1))
    limit = int(query.pop('limit', 20))
    level = int(query.pop('level', 0))
    if level and level > 0:
        objects = Event.objects.filter(level=level).order_by('-created')
    else:
        objects = Event.objects.filter(**query).order_by('-created')
    #objects = objects.filter(**query).order_by('-created')
   
    #if query:
    #    paginator = Paginator(objects.filter(**query)), limit, allow_empty_first_page=True)
    #else:
    #    
    paginator = Paginator(objects, limit, allow_empty_first_page=True)
    objs = []
    for p in paginator.page(start).object_list:#.all():
        #p.full_clean()
        #obj = p.to_python()
        #m = obj.pop('message')
        m = p.messages
        try:
            #obj['message'] = cjson.decode(m,True)
            p.messages = cjson.decode(m,True)
        except:
            pass
            #obj['message'] = m
        objs.append(p)
    data = {'objects': objs,
            'limit': limit,
            'start': start,
            "rate": int(query.get('refresh', 5)),
            'range': range(1, paginator.num_pages + 1),
            "version": settings.API_VERSION }
    return data

def logs(request,*args,**kwargs):
    data = _list(request)
    return render_to_response('web/logs.html', RequestContext(request,data))

def log_list(request):
    data = _list(request)
    return render_to_response('web/log_list.html', RequestContext(request,data))

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
