""" Handler extensions
"""
import logging
import cjson

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from mds.api import LOGGER
from mds.api.handlers import DispatchingHandler
from mds.api.decorators import logged
from mds.api.responses import succeed, fail, error
from mds.api.signals import EventSignal, EventSignalHandler
from mds.core.forms import SessionForm
from mds.core.models import Event

from .forms import ANMForm, PatientForm
from .models import ANM, Patient

__all__ = [
    "ANMSessionHandler",
    "ANMHandler",
    "PatientHandler"
    ]

@logged     
class ANMSessionHandler(DispatchingHandler):
    """ Handles session auth requests. """
    allowed_methods = ('POST',)
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    form = SessionForm
    #model = None
    
    def create(self,request):
        try:
            content_type = request.META.get('CONTENT_TYPE', None)
            logging.debug(content_type)
            is_json = 'json' in content_type
            logging.debug("is_json: %s" % is_json)
            if is_json:
                raw_data = request.read()
                data = cjson.decode(raw_data)
            else:
                data = self.flatten_dict(request.POST)
            
            username = data.get('username', 'empty')
            password = data.get('password','empty')
            if not settings.TARGET == 'SELF':
                instance = User(username=username)
                auth = {'username':username, 'password':password }
                result = backends.create('Session', auth, instance)
                if not result:
                    return fail([],errors=["Observer does not exist",],code=404)
                # Create a user or fetch existin and update password
                user,created = User.objects.get_or_create(username=result.user.username)
                user.set_password(password)
                user.save()
                
                # should have returned an Observer instance here
                observers = ANM.objects.filter(user__username=user.username)
                # If none were returned we need to create the Observer
                if observers.count() == 0:
                    observer = Observer(
                        user=user,
                        uuid = result.uuid)
                    observer.save()
                else:
                    # Observer already exists so we don't have to do 
                    # anything since password cache is updated
                    observer = observers[0]
                return succeed(list(observer))
            else:
                user = authenticate(username=username, password=password)
                if user is not None:
                    #observer = Observer.objects.get(user=user)
                    return succeed(ANM.objects.filter(user__username=user.username))
                else:
                    msg = "Invalid credentials"
                    logging.warn(msg)
                    return fail([], code=404, errors=[msg,])
        except Exception as e:
            msg = "Internal Server Error"
            logging.error(unicode(e))
            logtb()
            return error(msg)

@logged
class ANMHandler(DispatchingHandler):
    allowed_methods = ('GET', 'POST','PUT')
    model = ANM
    form = ANMForm
    fields = (
        "uuid",
        ("user",("username","is_superuser")),
        ("locations",("uuid", "name")),
        "modified",
        "created",
        "voided",
    )
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}

@logged
class PatientHandler(DispatchingHandler):
    allowed_methods = ('GET', 'POST','PUT')
    model = Patient
    form = PatientForm
    fields = (
        "uuid",
        "family_name",
        "given_name",
        "gender",
        "dob",
        "image",
        "system_id",
        "secondary_id",
        "caregiver_name",
        "secondary_caregiver_name",
        ("location",("name","uuid")),
        "modified",
        "created",
        "voided",
    )
    signals = { LOGGER:( EventSignal(), EventSignalHandler(Event))}
    
    def _update(self,request, uuid):
        '''Override super method to handle extra_data. Raw data stored
           should not be overridden if empty
        '''
        logging.info("_update() %s" % uuid)
        model = getattr(self,'model')
        data = request.raw_data
        if 'uuid' in data.keys():
            uuid = data.pop('uuid')
        
        qs = model.objects.filter(uuid=uuid)
        if qs.count() == 1:
            obj = qs[0]
            # 'extra_data' should be a write once if not None
            if obj.extra_data:
                data['extra_data'] = obj.extra_data
            qs.update(**data)
        # No objects found raise
        elif qs.count() == 0:
            raise ObjectDoesNotExist("{0} '{1}'".format(model.__name__, uuid)) 
        # more than one raise
        else:
            raise MultipleObjectsReturned("{0} '{1}'".format(model.__name__, uuid))
        return model.objects.get(uuid=uuid)
