'''
Created on Feb 29, 2012

:Authors: Sana Dev Team
:Version: 2.0
'''
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext_lazy as _


from piston.handler import BaseHandler

#from piston.utils import validate

from sana.api.decorators import validate
from sana.api.responses import succeed, error
from sana.api.utils import logstack, printstack, exception_value

__all__ = ['RESTHandler', ]

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
            instance = self._create_object(request, args, kwargs)  
            return succeed(instance.get_representation())
        except Exception, e:
            return self.trace(request, e)
      
    def read(self,request, uuid=None, related=None):
        """ GET Request handler. No validation is performed. """
        try:
            if uuid and related:
                response = self._read_by_uuid(request,uuid, related=related)
            elif uuid:
                response = self._read_by_uuid(request,uuid)
            else:
                response = self._read_multiple(request)
            return succeed(response)  
        except Exception, e:
            return self.trace(request, e)
        
    def update(self, request, uuid=None):
        """ PUT Request handler. Allows single item updates only. """
        try:
            if not uuid:
                raise Exception("UUID required for update.")
            msg = self._update(request, uuid)
            return succeed(msg)
        except Exception, e:
            return self.trace(request, e)
    
    def delete(self,request, uuid=None):
        """ DELETE Request handler. No validation is performed. """
        try:
            if not uuid:
                raise Exception("UUID required for delete.")
            msg = self._delete(uuid)
            return succeed(msg)
        except Exception, e:
            return self.trace(request, e)

    def trace(self,request, ex=None):
        try:
            if settings.DEBUG:
                printstack(ex)
            _,message,_ = logstack(self,ex)
            return error(message)
        except:
            return error(exception_value(ex))
    
    def _create(self,request, *args, **kwargs):
        data = request.form.cleaned_data
        klazz = getattr(self,'model')
        instance = klazz(**data)
        instance.save()          
        return instance
    
    
    def _read_multiple(self, request, *args, **kwargs):
        """ Returns a zero or more length list of objects.
        """
        rep, start, limit = get_REST_params(request)
        model = getattr(self,'model')
        obj_set = model.objects.all()
        if limit:
            paginator = Paginator(obj_set, limit, 
                                  allow_empty_first_page=True)
            try:
                objs = paginator.page(start).object_list
            except (EmptyPage, InvalidPage):
                objs = paginator.page(paginator.num_pages).object_list      
        else:
            objs = obj_set
        return [ x.get_representation(rep,location=get_root(request)) for x in objs ]

    def _read_by_uuid(self,request, uuid, related=None):
        """ Reads an object from the database using the UUID as a slug and 
            will return the object along with a set of related objects if 
            specified.
            
            Sending rep='full' will return all fk objects back to the instance.
        """
        rep, _,_ = get_REST_params(request)
        model = getattr(self.__class__, 'model')
        obj = model.objects.get(uuid=uuid)
        if related:
            rm = obj._meta._name_map[related][0].model
            result = obj.get_representation(rep,location=get_root(request))
            objs = rm.objects.filter(**{model.__name__.lower() : obj})
            result[related] = [ x.get_representation(rep,location=get_root(request)) for x in objs[:]]
        else:
            result = obj.get_representation(rep,location=get_root(request))
        return result      

    def _update(self,request, uuid):
        model = getattr(self,'model')
        if hasattr(request, 'form'):
            request.form.save()
        else:
            obj = model.objects.get(uuid=uuid)
            data = self.flatten_dict(request.POST)
            if 'uuid' in data.keys():
                data.pop('uuid')
            for k,v in data.items():
                setattr(obj,k,v)
            obj.save()
        msg = "Successfully updated  {0}: {1}".format(model.__class__.__name__,uuid)
        return msg
    
    def _delete(self,uuid):
        model = getattr(self,'model')
        model.objects.delete(uuid=uuid)
        return "Successfully deleted {0}: {1}".format(model.__class__.__name__,uuid)
