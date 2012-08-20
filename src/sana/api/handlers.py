'''
Created on Feb 29, 2012

:Authors: Sana Dev Team
:Version: 2.0
'''
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext_lazy as _


from piston.handler import BaseHandler
from piston.utils import validate

from sana.api.models import RESTModel
from sana.api.responses import succeed, fail
from sana.api.utils import logstack, printstack

__all__ = ['handler_uri_templates', 'RESTHandler', ]

class UnsupportedCRUDException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return self.value

def get_root(request):
    host = request.get_host()
    scheme = 'https' if request.is_secure() else 'http'
    result = scheme + '://' + host
    return result

def get_REST_params(request): 
    get = dict(request.GET.items())
    limit = int(get.get('limit', 0))
    start = int(get.get('start', 1))
    rep = get.get('rep', 'default')
    return rep, start, limit

     
class RESTHandler(BaseHandler):
    """Base HTTP handler for Sana api. Uses basic CRUD approach of the  
       django-piston api as a thin wrapper around class specific functions.
    """
    exclude = ['id', 'created', 'modified']
    allowed_methods = ('GET',)
    
    
    @validate('POST')
    def create(self,request, *args, **kwargs):
        """ POST Request handler. Requires valid form defined by model of  
            extending class.
        """
        try:
            return succeed(request.form.save().get_representation())
        except Exception, e:
            return self.trace(request, e)
      
    def read(self,request, uuid=None, related=None):
        """ GET Request handler. No validation is performed. """
        try:
            if uuid and related:
                response = self.readRelatedByUuid(request,uuid)
            elif uuid:
                response = self.readByUuid(request,uuid)
            else:
                response = self.readMultiple(request)
            return succeed(response)  
        except Exception, e:
            return self.trace(request, e)
    
    def update(self, request, *args, **kwargs):
        """ PUT Request handler. No validation is performed. """
        try:
            return succeed(BaseHandler.update(self, request, args, kwargs))
        except Exception, e:
            return self.trace(request, e)
    
    def delete(self,request, *args, **kwargs):
        """ DELETE Request handler. No validation is performed. """
        try:
            return succeed(BaseHandler.delete(self, request, args, kwargs))
        except Exception, e:
            return self.trace(request, e)

    def trace(self,request, error):
        printstack(error)
        logstack(self,error)
        return fail(error)
    
    def readMultiple(self, request, *args, **kwargs):
        
        rep, start, limit = get_REST_params(request)
        model = getattr(self,'model')
        obj_set = model.objects.all()
        if limit:
            paginator = Paginator(obj_set, limit, 
                                  allow_empty_first_page=True)
            try:
                objs = paginator.page(start)
            except (EmptyPage, InvalidPage):
                objs = paginator.page(paginator.num_pages)       
        else:
            objs = obj_set
        return [ x.get_representation(rep,location=get_root(request)) for x in objs ]

    def readByUuid(self,request, uuid, related=None):
        """ Reads an object from the database using the UUID as a slug and 
            will return the object along with a set of related objects if 
            specified.
            
            Sending rep='full' will return all fk objects back to the instance.
        """
        rep, start, limit = get_REST_params(request)
        model = getattr(self.__class__, 'model')
        obj = model.objects.get(uuid=uuid)
        if related:
            result = getattr(object, related+'_set', [])
        else:
            result = obj.get_representation(rep,location=get_root(request))
        return result      
 