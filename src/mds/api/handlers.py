'''
Created on Feb 29, 2012

:Authors: Sana Dev Team
:Version: 2.0
'''
import logging

from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from piston.handler import BaseHandler
from piston.utils import rc

from .decorators import validate
from .responses import succeed, error
from .utils import logstack, printstack, exception_value

__all__ = ['DispatchingHandler', ]

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

def get_start_limit(request): 
    get = dict(request.GET.items())
    limit = int(get.get('limit', 0))
    start = int(get.get('start', 1))
    return start, limit

     
class DispatchingHandler(BaseHandler):
    """Base HTTP handler for Sana api. Uses basic CRUD approach of the  
       django-piston api as a thin wrapper around class specific functions.
    """
    exclude = ['id', 'created',]
    allowed_methods = ('GET','POST','PUT','DELETE')

    def queryset(self, request, uuid=None, **kwargs):
        qs = self.model.objects.all()
        if uuid:
            return self.model.objects.get(uuid=uuid)
        if kwargs:
            qs.filter(**kwargs)
        return qs
        #return self.model.objects.all()
    
    @validate('POST')
    def create(self,request, uuid=None, *args, **kwargs):
        """ POST Request handler. Requires valid form defined by model of  
            extending class.
        """
        logging.info("create(): %s, %s" % (request.method,request.user))
        if uuid:
            return self.update(request,uuid=uuid)
        try:
            instance = self._create(request, args, kwargs)  
            logging.info('POST')
            return succeed(instance)
        except Exception, e:
            logging.error('ERROR')
            return self.trace(request, e)
      
    def read(self,request, uuid=None, related=None,*args,**kwargs):
        """ GET Request handler. No validation is performed. """
        logging.info("read: %s, %s" % (request.method,request.user))
        try:
            if uuid and related:
                response = self._read_by_uuid(request,uuid, related=related)
            elif uuid:
                response = self._read_by_uuid(request,uuid)
            else:
                q = request.REQUEST
                if q:
                    logging.info("q = %s" % q)
                    response = BaseHandler.read(self,request, **q)
                else:
                    logging.info("No querystring")
                    response = BaseHandler.read(self,request)
            return succeed(response)
        except Exception, e:
            return self.trace(request, e)
        
    def update(self, request, uuid=None):
        """ PUT Request handler. Allows single item updates only. """
        logging.info("update(): %s, %s" % (request.method,request.user))
        try:
            if not uuid:
                raise Exception("UUID required for update.")
            msg = self._update(request, uuid)
            return succeed(msg)
        except Exception, e:
            return self.trace(request, e)
    
    def delete(self,request, uuid=None):
        """ DELETE Request handler. No validation is performed. """
        logging.info("delete(): %s, %s" % (request.method,request.user))
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
                logging.error(ex)
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
        start, limit = get_start_limit(request)
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
        return objs

    def _read_by_uuid(self,request, uuid, related=None):
        """ Reads an object from the database using the UUID as a slug and 
            will return the object along with a set of related objects if 
            specified.
        """
        obj = BaseHandler.read(self,request,uuid=uuid)
        if not related:
            return obj
        return getattr(obj[0], str(related) + "_set").all()

    def _update(self,request, uuid):
        logging.info("_update() %s" % uuid)
        model = getattr(self,'model')
        if hasattr(request, 'form'):
            request.form.save()
            msg = "Successfully updated  {0}: {1}".format(model.__class__.__name__,uuid)
        else:
            obj = model.objects.get(uuid=uuid)
            data = self.flatten_dict(request.POST)
            if 'uuid' in data.keys():
                data.pop('uuid')
            for k,v in data.items():
                setattr(obj,k,v)
            obj.save()
            msg = obj
        
        return msg
    
    def _delete(self,uuid):
        model = getattr(self,'model')
        model.objects.delete(uuid=uuid)
        return "Successfully deleted {0}: {1}".format(model.__class__.__name__,uuid)
