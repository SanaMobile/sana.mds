import cjson
import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse

from django import forms
from django.forms.models import modelformset_factory, modelform_factory
from django.db.models import ForeignKey, FileField, ImageField, DateField, DateTimeField

from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.template.response import TemplateResponse 
from django.views.generic import *
from django.views.generic.detail import *
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.utils import translation 
from django.utils.datastructures import SortedDict

from extra_views import CreateWithInlinesView, UpdateWithInlinesView
from django.contrib.auth.models import User

from mds.api import version
from mds.api.responses import JSONResponse
from mds.api.v1.v2compatlib import sort_by_node
from mds.clients.models import Client
from mds.core.forms import *
from mds.core.models import *
from .forms import *
from mds.core.widgets import *
from mds.web.generic.filtering import FilterMixin
from .generic.sorting import SortMixin
from mds.tasks.models import *
from . import portal

from mds.utils.translation import *


CK_LANGUAGE = "language"
def set_cookie(response, key, value, days_expire = 7):
  if days_expire is None:
    max_age = 365 * 24 * 60 * 60  #one year
  else:
    max_age = days_expire * 24 * 60 * 60 
  expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

def set_lang(response, lang="en"):
    if not lang:
        lang = "en"
    set_cookie(response, CK_LANGUAGE, lang, days_expire = 365)

def login(request,*args,**kwargs):    
	
	# set the next page
    redirect_to = request.REQUEST.get("next", None)
    next_page = redirect_to if redirect_to else reverse("web:portal")
    
    # set the language
    lang = get_request_language(request)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        #lang = request.POST.get('language')
        
        activate(lang)
        user = authenticate(username=username, password=password)
        if user is None:
            response = TemplateResponse(request,
                'web/login.html'.format(lang=lang),
                {
                    'form': LoginForm(),
                    'next': next_page,
                    'lang': lang,
                })
            
        else:
            auth_login(request, user)
            response =  HttpResponseRedirect(next_page)

    else:
        response = TemplateResponse(request,
            'web/login.html',
            {
                'form': LoginForm(),
                'lang':lang,
                'available_languages' : get_available_languages(),
                'next': next_page,
            })
            
    # Update the cookie
    #activate(lang)
    response.set_cookie(settings.LANGUAGE_SESSION_KEY, lang)
    return response

def logout(request, *args, **kwargs):
	# set the language
    lang =  get_request_language(request)
    #lang = request.session.get(settings.LANGUAGE_SESSION_KEY, "en")
    auth_logout(request)
    url = reverse('web:login')
    activate(lang)
    response = redirect(url)
    #response.set_cookie(settings.LANGUAGE_SESSION_KEY, lang)
    return response

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

@login_required(login_url='/mds/web/login/')
def web_root(request, **kwargs):
    from mds.core import models as objects
    metadata = _metadata(request)
    lang = kwargs.get('lang','en')
    return render_to_response(
        "web/index.html".format(lang=lang), 
        context_instance=RequestContext(
            request,
            {
              'flavor': metadata.flavor,
              'errors': metadata.errors,
              'messages' : metadata.messages,
              'models' : objects.__all__,
              'portal': portal.nav(request),
              'lang': lang,
              'available_languages': get_available_languages(),
            }))

def registration(request, **kwargs):
    metadata = _metadata(request)
    lang = get_and_activate(request)
    return render_to_response(
        "web/registration.html".format(lang=lang), 
        context_instance=RequestContext(
            request,
            {
              'form':  SurgicalSubjectForm(),
              'flavor': metadata.flavor,
              'errors': metadata.errors,
              'messages' : metadata.messages,
              'portal': portal.nav(request),
              'lang':lang,
              'available_languages': get_available_languages(),
        }))

@login_required(login_url='/mds/web/login/')
def encounter_task(request, **kwargs):
    lang = get_and_activate(request)
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
    lang = kwargs.get('lang','en')
    return render_to_response(
        tmpl, 
        context_instance=RequestContext( 
            request, 
            {
             'form':form,
             'errors': errors,
             'portal': portal.nav(request),
             'language':lang,
              'available_languages': get_available_languages(),
            })
        )
# TODO make this better
# Procedure UUid tp form mappings
_procedure_forms = {
    "303a113c-6345-413f-88cb-aa6c4be3a07d": IntakeForm,
}

@login_required(login_url='/mds/web/login/')
def edit_encounter_task(request, uuid, **kwargs):
    lang = get_and_activate(request)
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
                                 #'debug' : debug,
                                 'portal': portal.nav(request),
                                 'lang': lang,
                                 'available_languages': get_available_languages(),
                                })
                             )
@login_required(login_url='/mds/web/login/')
def web_encounter(request, **kwargs):
    lang = get_and_activate(request)
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
    
    extra_forms = [InitialTaskSetForm(),]


    return render_to_response("web/encounter_form.html".format(lang=lang), 
                              context_instance=RequestContext( request, 
                                {
                                 'form': form,
                                 'extra_forms': extra_forms,
                                 'flavor': flavor,
                                 'errors': errors,
                                 'portal': portal.nav(request),
                                 'lang': lang,
                                 'available_languages': get_available_languages(),
                                })
                             )

@login_required(login_url='/mds/web/login/')
def task_list(request):
    lang = get_and_activate(request)
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
    prange = range(1,paginator.num_pages + 1)
    lang = kwargs.get('lang','en')
    return render_to_response("web/etask_list.html", 
                              context_instance=RequestContext( request, 
                                {
                                 'tasks':tasks.object_list,
                                 'range':prange,
                                 'page': page,
                                 'available_languages': get_available_languages(),
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
    lang = get_and_activate(request)
    data = _list(request)
    data['portal'] = portal.nav(request)
    data['lang'] = kwargs.get('lang','en')
    data['available_languages'] = get_available_languages()
    return render_to_response('web/logs.html'.format(lang=data['lang']), RequestContext(request,data))

def log_list(request):
    data = _list(request)
    data['available_languages'] = get_available_languages()
    lang = kwargs.get('lang','en')
    return render_to_response('web/log_list.html'.format(lang=lang),
        RequestContext(request,data))

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
    lang = get_and_activate(request)
    query = dict(request.GET.items())
    page = int(query.get('page', 1))
    page_size = int(query.get('page_size', 20))
    
    data = {'object_list': {},
            'page_range': range(0, 1),
            'page_size': page_size,
            'page': page,
            'available_languages': get_available_languages(),
            "rate": int(query.get('refresh', 5)) }
    return render_to_response('logging/index.html', RequestContext(request,data))


########################################################################
# Class based views
########################################################################
#class @ListView(ListView):
#    model = @
#    template_name = "web/@_list.html"
#
#class @CreateView(CreateView):
#    model = @
#    template_name = "web/@_edit.html"
    

_core = [
    Concept,
    Device,
    Encounter,
    Location,
    Notification, 
    Observation, 
    Observer,
    Procedure,
    Subject,
]

_tasks = [
    EncounterTask,
]


class TranslationMixin(object):
    lang = 'en'
    def __init__(self,*args, **kwargs):
        super(TranslationMixin,self)

    def dispatch(self, request, *args, **kwargs):
        self.lang = get_and_activate(request)
        request.session[settings.LANGUAGE_SESSION_KEY] = self.lang
        return super(TranslationMixin, self).dispatch(request,*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TranslationMixin, self).get_context_data(**kwargs)
        context['lang'] = self.lang
        #context[settings.LANGUAGE_FIELD_NAME] = self.lang
        context['available_languages'] = get_available_languages()
        return context

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view,login_url='/mds/web/login/')

class ModelListMixin(TranslationMixin, LoginRequiredMixin,  SortMixin ):
    template_name = "web/list.html"
    exclude = ()
    _fields = []
    default_sort_params = ('created', 'asc')
    
    def __init__(self, *args, **kwargs):
        super(ModelListMixin,self)
        self._fields = self.field_names()
        if not hasattr(self,'form'):
            self.form = modelform_factory(self.model)
        if not hasattr(self,'exclude'):
            self.exclude = ()
        #template = getattr(self, 'template_name')
        #setattr(self, 'template_name', template.format(lang=self.lang))

    def field_names(self):
        if not getattr(self,'fields',None):
            return list(x.name for x in self.model._meta.fields)
        else:
            return self.fields

    def get_object_dict(self, obj):
        opts = obj._meta
        _obj = SortedDict()
        fields = SortedDict()
        for f in self._fields:
            #field = getattr(obj._meta, f, None)
            field = opts.get_field(f)
            data = {
                    'label_tag': f.replace("_"," "),
                    'is_link': False,
                    'value': getattr(obj, f),
                    'url': None,
                    'type': 'text',
            }
            if isinstance(field, ForeignKey):
                field_obj = getattr(obj,f)
                data['is_link'] = True
                if field_obj:
                    data['url'] = u'/mds/web/{model}/{uuid}/'.format(
                        model=field_obj.__class__.__name__.lower(),
                        uuid=unicode(field_obj.id))
                data['type'] = 'object'
            elif isinstance(field, FileField):
                data['is_link'] = True
                data['url'] = u'/mds/media/{path}'.format(
                    path=unicode(getattr(obj, f)))
                data['type'] = 'file'
            elif isinstance(field, DateField):
                data['type'] = 'date'
            elif isinstance(field, DateTimeField):
                data['type'] = 'date'
            fields[f] = data
        _obj['fields'] = fields
        _obj['id'] = obj.id
        _obj['repr'] = unicode(obj)
        return _obj

    def get_context_data(self, **kwargs):
        context = super(ModelListMixin, self).get_context_data(**kwargs)
        context['model'] = self.model.__name__.lower()
        #context['form'] = self.form(self.object)
        #context['fields'] = self._fields
        labels = {}
        for x in self.model._meta.fields:
            labels[x.name] = x.verbose_name
        
        context['fields'] = [ labels[x] for x in self._fields ]
        
        #    context['fields'] = [y.verbose_name for y in [ getattr(self.model, x) for x in self._fields]]
        if context.has_key('object'):
            context['object_list'] = [context['object'],]
        context['objects'] = [self.get_object_dict(x) for x in context['object_list']]
        #sort_by, order = self.get_sort_params()
        #context.update({'sort_by': sort_by, 'order': order})
        context['portal'] = portal.nav(getattr(self,'role',None))
        return context

class ModelMixin(object):
    template_name = "web/form.html"
    
    def __init__(self, *args, **kwargs):
        super(ModelMixin,self)
    #    if not hasattr(self,'fields'):
    #        self.fields = self.get_default_model_fields()
    #    if not hasattr(self,'form'):
    #        self.form =  modelform_factory(self.model, fields=self.fields)

    def get_context_data(self, **kwargs):
        context = super(ModelMixin, self).get_context_data(**kwargs)
        context['model'] = self.model.__name__.lower()
        return context
        
class ModelFormMixin(TranslationMixin, LoginRequiredMixin):
    template_name = "web/form.html"
    default_sort_params = ('created', 'asc')
    exclude = ()
    _fields = []
    success_url_format = "/{app}/{model}/%(id)s/"
    app = 'mds.web'
    
    def __init__(self, *args, **kwargs):
        super(ModelFormMixin,self)
        #if not hasattr(self,'fields'):
        #    self.fields = self.get_default_model_fields()
        self._fields = self.field_names()
        if not hasattr(self,'form'):
            self.form = modelform_factory(self.model)
        if not hasattr(self,'exclude'):
            self.exclude = ()
        
        _app=getattr(self,'app').replace(".","/")
        _model = getattr(self,"model").__name__.lower()
        setattr(self,'success_url', 
                self.success_url_format.format(app=_app,model=_model))

    def field_names(self):
        if not getattr(self,'fields',None):
            return [x.name for x in self.model._meta.fields]
        else:
            return self.fields

    def get_field_list(self, obj):
        from django.utils.datastructures import SortedDict
        form = self.form(instance=obj)
        opts = obj._meta
        fields = SortedDict()
        objs = SortedDict()
        for field in self._fields:
            _obj = {}
            if not field.name in self.exclude:
                data = {
                    'name': field.name,
                    'is_link': False,
                    'value': getattr(obj,field.name),
                    'link': None,
                    'secure': False,
                }
                if isinstance(field.widget, forms.PasswordInput):
                    data['secure'] = True
                if isinstance(field, ForeignKey):
                    data['is_link'] = True
                    related = getattr(obj,field.name)
                    if related:
                        data['link'] = u'/mds/web/{model}/{uuid}/'.format(
                            model=field.model,
                            uuid=unicode(related.id))
                elif isinstance(field, FileField):
                    data['is_link'] = True
                    data['link'] = u'/mds/media/{path}'.format(
                        path=unicode(getattr(obj,field.name)
                        ))
                _obj[field.name] = data
                objs.append(_obj)
        return tuple(fields)

    def get_object_dict(self, obj):
        opts = obj._meta
        from django.utils.datastructures import SortedDict
        _obj = SortedDict()
        fields = SortedDict()
        for f in self._fields:
            field = getattr(opts, f, None)
            _field = None
            for x in obj._meta.fields:
                if x.name == f:
                    _field = x
            #_field = type(f)
            data = {
                    'label_tag': f.replace("_"," "),
                    'is_link': False,
                    'value': getattr(obj, f),
                    'url': None,
                    'type': _field,
                    'secure': False,
                    'input_type': 'text',
            }
            if isinstance(_field, ForeignKey):
                related = getattr(obj, f)
                data['is_link'] = True
                if related:
                    data['url'] = u'/mds/web/{model}/{uuid}/'.format(
                        model= f.lower(), 
                        uuid=unicode(related.id))
                data['type'] = 'ref'
            elif isinstance(_field, FileField):
                data['is_link'] = True
                data['url'] = u'/mds/media/{path}'.format(
                    path=unicode(getattr(obj, f)))
                data['type'] = 'file'
            elif isinstance(_field, DateField):
                data['type'] = 'date'
            elif isinstance(_field, DateTimeField):
                data['type'] = 'date'
            fields[f] = data
        _obj['fields'] = fields
        _obj['id'] = obj.id
        _obj['repr'] = unicode(obj)
        return _obj

    def get_context_data(self, **kwargs):
        context = super(ModelFormMixin, self).get_context_data(**kwargs)
        context['model'] = self.model.__name__.lower()
        context['fields'] = self._fields
        if context.has_key('object'):
            context['objects'] = [self.get_object_dict(context['object']),]
        if context.has_key('object_list'):
            context['objects'] = [ self.get_object_dict(x) for x in context['object_list']]
        context['portal'] = portal.nav(getattr(self,'role',None))

        context['lang'] = self.kwargs.get('lang','en')
        return context
        
class ModelSuccessMixin(SuccessMessageMixin):
    success_message = "%(model)s: %(uuid)s was updated successfully"

    def get_success_message(self, cleaned_data):
        klazz = getattr(self,'model',None)
        if klazz:
            klazz = klazz.__name__
        else:
            klazz = _('Object')
        data = {
            'model': klazz,
            'uuid' : self.object.uuid
            }
        return self.success_message % (data)

# Concepts
class UserListView(ModelListMixin, ListView):
    model = User
    template_name = "web/list.html"
    fields = ('username','last_name','first_name',)
    paginate_by=10
    default_sort_params = ('username','last_name',)

class UserCreateView(SuccessMessageMixin,CreateView):
    model = User
    template_name = "web/form_user_new.html"
    form_class = UserForm
    success_message = "User: %(username)s was created successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data)
        
    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['model'] = self.model.__name__.lower()
        context['portal'] = portal.nav(getattr(self,'role',None))
        return context

class UserUpdateView(ModelFormMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'web/form_user.html'
    form_class = UserForm

    success_message = "User: %(username)s was updated successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data)

class UserDetailView(ModelFormMixin,DetailView):
    model = User
    template_name = 'web/detail.html'
    context_object_name = 'user'
    slug_field = 'uuid'
    fields = ('username','last_name','first_name','email')

# Concepts
class ConceptListView(ModelListMixin, ListView):
    model = Concept
    template_name = "web/list.html"
    fields = ('created', 'name', 'description', 'voided')
    paginate_by=10

class ConceptCreateView(ModelFormMixin,SuccessMessageMixin,CreateView):
    model = Concept
    template_name = "web/form_new.html"

class ConceptUpdateView(ModelFormMixin, SuccessMessageMixin, UpdateView):
    model = Concept
    template_name = 'web/form.html'
    success_message = _("Concept was updated successfully") + ": %(name)s"
    
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data)
        
class ConceptDetailView(ModelFormMixin,DetailView):
    model = Concept
    template_name = 'web/detail.html'
    context_object_name = 'concept'
    slug_field = 'uuid'

# Devices
class DeviceListView(ModelListMixin, ListView):
    model = Device
    template_name = "web/list.html"
    fields = ('created','name','voided',)
    paginate_by=10

class DeviceCreateView(ModelFormMixin,CreateView):
    model = Device
    template_name = "web/form_new.html"

class DeviceUpdateView(ModelFormMixin, UpdateView):
    model = Device
    template_name = 'web/form.html'

class DeviceDetailView(ModelFormMixin, DetailView):
    model = Device
    template_name = 'web/detail.html'
    context_object_name = 'device'
    slug_field = 'uuid'

# Encounters
class EncounterListView(ModelListMixin,ListView):
    model = Encounter
    template_name = "web/list.html"
    fields = ('created', 'procedure', 'subject')
    paginate_by=10
    
class EncounterCreateView(ModelFormMixin,ModelSuccessMixin, CreateView):
    model = Encounter
    template_name = "web/form_new.html"

class EncounterUpdateView(ModelFormMixin, ModelSuccessMixin, UpdateView):
    model = Encounter
    template_name = "web/form.html"

class EncounterDetailView(ModelFormMixin,DetailView):
    model = Encounter
    template_name = 'web/encounter_detail.html'
    context_object_name = 'encounter'
    slug_field = 'uuid'

# Locations
class LocationListView(ModelListMixin, ListView):
    model = Location
    template_name = "web/list.html"
    paginate_by=10
    default_sort_params = ('name', 'asc')
    fields = ('name','code',)
    
class LocationCreateView(ModelFormMixin,ModelSuccessMixin,CreateView):
    model = Location
    template_name = "web/form_new.html"
    #success_url="/mds/web/location/%(id)s/"
    
class LocationUpdateView(ModelFormMixin, ModelSuccessMixin,UpdateView):
    model = Location
    template_name = 'web/form.html'
    #success_url='/mds/web/location/%(id)s/'
    
class LocationDetailView(ModelFormMixin,ModelSuccessMixin,DetailView):
    model = Location
    template_name = 'web/detail.html'
    context_object_name = 'location'
    slug_field = 'uuid'

# Observations
class ObservationListView(ModelListMixin, ListView):
    model = Observation
    template_name = "web/list.html"
    paginate_by=10
    fields = (
        'created',
        'encounter',
        'node',
        'concept',
        'value_text',
        'value_complex',
    )

class ObservationCreateView(ModelFormMixin,ModelSuccessMixin,CreateView):
    model = Observation
    template_name = "web/form_new.html"

class ObservationUpdateView(ModelFormMixin, ModelSuccessMixin, UpdateView):
    model = Observation
    template_name = 'web/form.html'

class ObservationDetailView(ModelFormMixin,DetailView):
    model = Observation
    template_name = 'web/detail.html'
    context_object_name = 'observation'
    slug_field = 'uuid'

# Observers
class ObserverListView(ModelListMixin, ListView):
    model = Observer
    template_name = "web/list.html"
    paginate_by=10

class ObserverCreateView(ModelFormMixin,ModelSuccessMixin,CreateView):
    model = Observer
    template_name = "web/form_new.html"
    
class ObserverUpdateView(ModelFormMixin, ModelSuccessMixin,UpdateView):
    model = Observer
    template_name = 'web/form.html'

class ObserverDetailView(ModelFormMixin,ModelSuccessMixin,DetailView):
    model = Observer
    template_name = 'web/detail.html'
    context_object_name = 'observer'
    slug_field = 'uuid'

# Procedures
class ProcedureListView(ModelListMixin, ListView):
    template_name = 'web/list.html'
    model = Procedure
    default_sort_params = ('title', 'asc')
    fields = ('title', 'version', 'author', 'src')#,'uuid')
    paginate_by=3

        
class ProcedureDetailView(ModelFormMixin,DetailView):
    model = Procedure
    template_name = 'web/detail.html'
    context_object_name = 'procedure'
    slug_field = 'uuid'
    
class ProcedureCreateView(ModelFormMixin,ModelSuccessMixin,CreateView):
    model = Procedure
    template_name = "web/form_new.html"

class ProcedureUpdateView(ModelFormMixin,ModelSuccessMixin, UpdateView):
    model = Procedure
    template_name = 'web/form.html'

class SubjectListView(ModelListMixin, ListView):
    model = Subject
    default_sort_params = ('system_id', 'asc')
    fields = ('system_id', 'family_name', 'given_name', 'gender', 'dob','voided')
    template_name = "web/list_subjects.html"
    paginate_by=10

class SubjectCreateView(ModelFormMixin,ModelSuccessMixin,CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "web/form_new.html"

class SubjectUpdateView(ModelFormMixin, ModelSuccessMixin,UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'web/form.html'

class SubjectDetailView(ModelFormMixin,DetailView):
    model = Subject
    template_name = 'web/detail.html'
    context_object_name = 'subject'
    slug_field = 'uuid'

class EncounterTaskListView(ModelListMixin, ListView):
    model = EncounterTask
    default_sort_params = ('due_on', 'asc')
    fields = ('due_on', 'status', 'subject', 'assigned_to')
    template_name = "web/task_list.html"
    paginate_by=10

    def get_queryset(self):
        qs = EncounterTask.objects.all()
        status = self.request.GET.get('status',None)
        if status:
            setattr(self,'status',status)
            return qs.filter(status__id=int(status))
        else:
            return qs

    def get_context_data(self, **kwargs):
        context = super(EncounterTaskListView,self).get_context_data(**kwargs)
        if hasattr(self,'status'):
            context['status'] = self.status
        
        for obj in context['objects']:
            due_on = obj['fields'].get('due_on')['value']
            twindow = datetime.timedelta(days=1)
            days = (datetime.datetime.today() - due_on).days
            if (days >= 1):
                obj['late'] = 'late'
            elif (days < 1) and (days >= 0):
                obj['late'] = 'today'
        return context

class EncounterTaskCreateView(ModelFormMixin,ModelSuccessMixin,CreateView):
    model = EncounterTask
    template_name = "web/form_new.html"
    form_class = EncounterTaskForm
    
    #def form_valid(self, form):
    #    concept = Concept.objects.get(uuid=form.instance.concept.uuid)
    #    form.instance.concept = concept
    #    return super(EncounterTaskCreateView, self).form_valid(form)

class EncounterTaskUpdateView(ModelFormMixin,ModelSuccessMixin, UpdateView):
    model = EncounterTask
    template_name = 'web/form.html'
    form_class = EncounterTaskForm

class EncounterTaskDetailView(ModelFormMixin,DetailView):
    model = EncounterTask
    template_name = 'web/encountertask_detail.html'
    context_object_name = 'encountertask'
    slug_field = 'uuid'

    def get_context_data(self, **kwargs):
        context = super(EncounterTaskDetailView, self).get_context_data(**kwargs)
        encounter = context['object'].encounter
        observations = None
        if encounter:
            observations = sort_by_node(encounter.observations.all())[::-1]
        context['related'] = observations
        context['related_label'] = 'Observations'
        return context

# class @ListView(ListView):
#     model = @
#     template_name = "web/@_list.html"

def surgeon_clinic_form(request, *args, **kwargs):
    params = request.COOKIES
    # Should use this to track IP's?
    device = params.get('device', "2fc0a9f7-384b-4d97-8c1c-aa08f0e12105")
    #if device:
    #    device = Device.objects.get(uuid=device)
    patients = Subject.objects.filter(voided=False)
    
    lang = get_and_activate(request)
    tmpl = "web/surgical_clinic_form.html"
    return render_to_response(
        tmpl,
        context_instance=RequestContext(
            request, 
            {
                'portal':portal.nav(request),
                'patients': patients,
                'device': device,
                'procedure': None,
                'lang': lang,
                'available_languages': get_available_languages(),
            }
        )
    )

@login_required(login_url="/mds/web/login/")
def setlang(request, *args, **kwargs):
    method = request.method
    if method == 'GET':
        lang = get_and_activate(request)
        path = request.REQUEST.get('next',reverse('web:portal'))
        languages = get_available_languages()
        return render_to_response(
            "web/setlang.html",
            context_instance=RequestContext(
                request, 
                {
                    'available_languages': languages,
                    'portal':portal.nav(request),
                    'next': path,
                    'lang': lang,
                    'available_languages': get_available_languages(),
                }))

    elif method == 'POST':
        path = request.POST.get('next', reverse('web:portal'))
        lang = request.POST.get('language', "en")
        activate(lang)
        
        response = HttpResponseRedirect(path)
        # set the language cookie here
        response.set_cookie(settings.LANGUAGE_SESSION_KEY,lang)
        return response

class PortalView(TranslationMixin, LoginRequiredMixin, TemplateView):
    template_name = 'web/index.html'
    
    def get_context_data(self,*args,**kwargs):
        context = super(PortalView,self).get_context_data(*args,**kwargs)
        context['portal'] = portal.nav(self.request)
        return context

class PortalListView(TranslationMixin, LoginRequiredMixin, ListView):
    template_name = 'web/index.html'

class PortalCreateView(TranslationMixin, LoginRequiredMixin, CreateView):
    template_name = 'web/form_new.html'

class PortalUpdateView(TranslationMixin, LoginRequiredMixin, UpdateView):
    template_name = 'web/form.html'
    
@login_required(login_url="/mds/web/login/")
def portal_index(request,*args,**kwargs):
    from mds.core import models as objects
    metadata = _metadata(request)
    #lang = request.session.get(settings.LANGUAGE_SESSION_KEY)
    lang = get_and_activate(request)
    template = 'web/index.html'
    context = {
        'flavor': metadata.flavor,
        'errors': metadata.errors,
        'messages' : metadata.messages,
        'models' : objects.__all__,
        'lang': lang,
        'available_languages': get_available_languages(),
    }
    
    context['portal'] = portal.nav(request)
    response =  TemplateResponse(request,
        template,
        context,
    )
    return response

class PortalDefaultRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('portal', current_app='web')


@login_required(login_url="/mds/web/login/")
def encounter_review(request,**kwargs):
    lang = kwargs.get('lang','en')
    tmpl = 'web/surgical_encounter_review.html'
    uuid = kwargs.get('uuid',None) if kwargs else None
    messages = []
    try:
        encounter = Encounter.objects.get(uuid=uuid)
        data = []
        
        encounters = [encounter,]
        obsqs = Observation.objects.filter(encounter=encounter.uuid)
        observations = sort_by_node(obsqs,descending=False)
    except Exception, e:
        encounter = None
        observations = []
        messages = [ unicode(e), ]
    return render_to_response(
        tmpl, 
        context_instance=RequestContext(
            request,
            { 
                'object': encounter,
                "observations": observations , 
                'portal': portal.nav(request),
                'messages': messages,
                'lang' :  lang,
                'available_languages': get_available_languages(),
            }))

class ClientDownloadsView(TemplateView):

    template_name = "web/download.html"

    def get_context_data(self, **kwargs):
        context = super(ClientDownloadsView, self).get_context_data(**kwargs)
        context['title'] = _("Mobile Client Downloads")
        context['objects'] = Client.objects.order_by("-version")
        context['portal'] = portal.nav(getattr(self,'role',None))
        context['lang'] = self.kwargs.get('lang','en')
        context['available_languages'] = get_available_languages()
        return context
