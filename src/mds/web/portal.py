'''


'''
import copy

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.response import TemplateResponse

from django.utils import six
from django.utils.decorators import classonlymethod
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django.utils import six
from django.views import generic
from django.conf import settings

__all__ = [
    'generate',
    'nav',
    'NavMixin',
]

def build_urls(model_list):
    pass
    
class Portal(object):

    app = None
    label = None
    sites = {}
    _sites = []
    _urlcache = None

    @property
    def urls(self):
        pass
    
    def __init__(self, app, name, sites=None):
        self.app = app
        self.name = name
        if sites:
            self.sites = sites
            
    @classonlymethod
    def autocreate(cls):
        pass

    def render(self, user):
        _rendered = {
            'app': self.app,
            'name': self.name,
            'sites': []
        }
        sites = []
        groups = user.groups
        for site in self._sites:
            _site = self.sites.get(site)
            requires = _site('requires', None)
            if requires and not requires in groups:
                continue
            else:
                views = []
                _views = _site.get('views',[])
                for _view in _views:
                    requires = _view('requires', None)
                    if requires and not requires in groups:
                        continue
                    else:
                        views.append(_view)
                sites.append(_site)
        rendered['sites'] = sites
        return rendered
    
    def _get_site(self, site):
        return self.sites.get(site,{})
    
    def _get_views(self,site):
        return self._get_site(site).values()

    def register_site(self, site, requires=None, views=None):
        _views = views if views else []
        self.sites[site] = {
            'label': site,
            'requires': requires,
            'views': _views,
        }
        _sites.append(site)
        
    def register_view(self, site, label, context_name, requires=None, url=None):
        if not self.sites.has_key(site):
            self.register_site(site,requires=requires)
        _site = self._get_site(site)
        _view = {
            'label':label,
            'context_name': context_name, 
            'requires': requires,
            'url': url
        }
        _site['views'].append(_view)
        
    def register_model(self,model, view=None, app=None,**kwargs):
        pass
        
    def register_manager(self, model, view=None, app=None, **kwargs):
        pass
    
    def register_report(self, report, **kwargs):
        pass
    
    def register_form(self,form,**kwargs):
        pass
        
    def register_task(self,model,**kwargs):
        pass

class PortalView(object):

    exclude = ()
    fields = ()
    form = None
    opts = {}
    requires = None
    name = None
    model = None
    
    def __init__(self, name, **options):
        super(PortalSite,self)
        self.model = model
        self.name = name
        self.opts = copy.deepcopy(options)
    
    @property
    def name(self):
        return self.name



def PortalModelView(PortalView):
    

    def __init__(self, model, form=None, **opts):
        super(PortalModelView, self)

    @property
    def url(self):
        pass
        
    def edit_view(self, slug):
        pass
        
    def create_view(self, slug):
        pass
        
    def update_view(self, slug):
        pass
        
    def list_view(self, slug):
        pass
    
def PortalReportView(PortalView):
    pass

class PortalSite(object):
    
    class NavItem(object):
        label = None
        url = None
        children = []
        
        def __init__(self, label=None, url=None):
            super(NavItem, self)
            self.label = label if label else None
            self.url = url if url else None

    def __init__(self, name='portal',  **kwargs):
        super(PortalSite,self)
        self.name = name
        opts = copy.deepcopy(kwargs)
    
    urlpatterns = None
    name = None
    _registry = {}
    opts = {}
    @property
    def sidebar(self):
        ''' Return a list of menu items to include in a sidebar menu.
        '''
        pass

    def home(self, request, extra_context=None):
        pass

    def register(self, model_or_iterable, portal_class=None, **options):
        pass

    def get_urls(self):
        from django.conf.urls import patterns, url, include

        #if settings.DEBUG:
        #    self.check_dependencies()

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        # Admin-site-wide views.
        urlpatterns = patterns('',
            url(r'^$',
                wrap(self.index),
                name='index'),
            url(r'^logout/$',
                wrap(self.logout),
                name='logout'),
        )

        # Add in each model's views.
        for model, model_admin in six.iteritems(self._registry):
            urlpatterns += patterns('',
                url(r'^%s/%s/' % (model._meta.app_label, model._meta.model_name),
                    include(model_admin.urls))
            )
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name
        
    @property
    def login(self):
        pass
        
    @property
    def logout(self):
        pass
        
        
    def register(self, portal_view,  **options):
        pass
        
EMPTY = {
        'name' : _('MDS2 Web Portal'),
        'app' : 'web',
        'sites' : []
        }

USERS = {
                'label':_('Users'),
                'requires': 'admin',
                'views': [
                    { 
                        'label': _('View all users'),
                        'context_name':'web:user-list',
                        'requires': None,
                    },
                    { 
                        'label': _('All Observers'),
                        'context_name':'web:observer-list',
                    },
                    { 
                        'label': _('New Observer'),
                        'context_name':'web:observer-create',
                    }
                ]
            }

site = {
        'name' : _('MDS2 Web Portal'),
        'app' : 'web',
        'sites' : [
            {
                'label':_('Data'),
                'requires': None,
                'views': [
                    { 
                        'label': _('concepts'),
                        'context_name':'web:concept-list',
                    },
                    { 
                        'label': _('devices'),
                        'context_name':'web:device-list',
                    },
                    { 
                        'label': _('encounters'),
                        'context_name':'web:encounter-list',
                    },
                    { 
                        'label': _('locations'),
                        'context_name':'web:location-list',
                    },
                    { 
                        'label': _('observations'),
                        'context_name':'web:observation-list',
                    },
                    { 
                        'label': _('patients'),
                        'context_name':'web:subject-list',
                    },
                    { 
                        'label': _('procedures'),
                        'context_name':'web:procedure-list',
                    },
                    #{ 
                    #    'label': _('encounter reviews'),
                    #    'context_name':'web:encounterreview-list',
                    #},
                ]
            },

            {
                'label': _('Tasks'),
                'requires': None,
                'views': [
                    { 
                        'label': _('Assigned'),
                        'context_name':'web:encountertask-list',
                    },
                    { 
                        'label': _('New'),
                        'context_name':'web:encountertask-create',
                    }
                ]
            },
            {
                'label':_('Forms'),
                'requires': None,
                'views':[
                    { 
                        'label': _('Intake Form'),
                        'context_name':'web:intake',
                    },
                    { 
                        'label': _('Patient Registration'),
                        'context_name':'web:register-patient',
                    },
                    { 
                        'label': _('Clinic Form'),
                        'context_name':'web:clinic-form',
                    }
                ]
            },
            {
                'label':_('Reports'),
                'views':[
                    { 
                        'label': _('Patient Visits'),
                        'context_name':'web:report-visits',
                    },
                    { 
                        'label': _('Unconfirmed Patients'),
                        'context_name':'web:form-subject-confirm',
                    }
                
                ]
            },
            {
                'label':_('Admin'),
                'requires': [ 'admin', ],
                'views':[
                    { 
                        'label': _('Downloads'),
                        'context_name':'web:download-client',
                    },
                    { 
                        'label': _('Logs'),
                        'context_name':'web:log-index',
                    },
                    #{ 
                    #    'label': _('Default Admin'),
                    #    'context_name': 'admin:index',
                    #}
                ]
            },
        ]
    }

SUPERVISOR = {
        'name' : _('MDS2 Web Portal'),
        'app' : 'web',
        'sites' : [
            {
                'label':_('Forms'),
                'requires': None,
                'views':[
                    { 
                        'label': _('Patient Registration'),
                        'context_name':'web:register-patient',
                    },
                    { 
                        'label': _('Intake Form'),
                        'context_name':'web:intake',
                    },
                    { 
                        'label': _('New Visit'),
                        'context_name':'web:encountertask-create',
                    },
                    { 
                        'label': _('Clinic Form'),
                        'context_name':'web:clinic-form',
                    },
                ]
            },
            {
                'label':_('Reports'),
                'views':[
                    { 
                        'label': _('Patient Visits'),
                        'context_name':'web:report-visits',
                    },
                    { 
                        'label': _('Unconfirmed Patients'),
                        'context_name':'web:form-subject-confirm',
                    }
                
                ]
            },
        ]
    }

SURGEON = {
        'name' : _('MDS2 Web Portal'),
        'app' : 'web',
        'sites' : [
            {
                'label':_('Reports'),
                'views':[
                    { 
                        'label': _('Patient Visits'),
                        'context_name':'web:report-visits',
                    },
                    { 
                        'label': _('Unconfirmed Patients'),
                        'context_name':'web:form-subject-confirm',
                    }
                ]
            },
        ]
    }

_portal = None

def detailview_factory(model, form_class=None, fields=None):
    pass
    
def createview_factory(model, form_class=None, fields=None):
    pass
    
def listview_factory(model, form_class=None, fields=None):
    pass

def updateview_factory(model, form_class=None, fields=None):
    pass

def get_or_create_portal(portal_site=None):
    if not _portal:
        _portal = portal_site if portal_site else PortalSite()

    _portal.register(portal_view, **options)

def generate(request, *args, **kwargs):
    pass

def is_in_group(group,user):
    if not user or not group:
        return False
    return user.groups.filter(name=group).exists()

def is_admin(user):
    return is_in_group("admin", user)

def is_supervisor(user):
    return is_in_group("supervisor", user)

def is_surgeon(user):
    return is_in_group("surgeon", user)
    
def is_developer(user):
    return is_in_group("developer", user)

def nav(request, *args, **kwargs):
    if request and not request.user:
        return _empty
    user = request.user
    if is_surgeon(user):
        return SURGEON
    elif is_supervisor(user):
        return SUPERVISOR
    elif is_admin(user):
        return site
    else:
        return EMPTY


def NavMixin(object):

    def dispatch(self,request,*args,**kwargs):
        setattr(self,'nav', nav(request))
        super(NavMixin,self).dispatch(request, *args, **kwargs)
