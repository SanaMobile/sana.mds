'''
Response definitions.

Created on Feb 29, 2012

:Authors: Sana Dev Team
:Version: 1.2
'''
import cjson
try:
    import json
except ImportError:
    import simplejson as json

from django.conf import settings
from django.http import HttpResponse
from django.template import loader

from sana.api.responses import fail, succeed

__all__ = ['json_fail', 'json_succeed',  'render_json_response', 
           'json_savedprocedure_succeed']

def json_fail(message):
    """Creates a formatted failure response. Response format::
    
        {'status':'FAILURE', 'message': message }
    
    Parameters:
        message
            Response message body
    
    """
    return cjson.encode(fail(message))

def json_succeed(message, encounter=None):
    """Creates a formatted success response. Response format:: 
    
        {'status':'SUCCESS', 'message': message }
    
    Parameters:
        message
            The response message body
    """
    response = succeed(message)
    if encounter:
        response['encounter'] = encounter
    return cjson.encode(response)

def render_json_response(data):
    """Sends an HttpResponse with the X-JSON header and the right mimetype.
    
    Parameters:
        data
            message content
    """
    resp = HttpResponse(data, mimetype=("application/json; charset=" +
                                        settings.DEFAULT_CHARSET))
    resp['X-JSON'] = data
    return resp

def render_json_template(*args, **kwargs):
    """Renders a JSON template, and then calls render_json_response(). 
    
    Parameters:
        args
            list of items to render 
        kwargs
            keyword/value pairs to render
    """
    data = loader.render_to_string(*args, **kwargs)
    return render_json_response(data)

def json_savedprocedure_succeed(savedproc_guid, encounter, data):
    """Creates a formatted success response for returning encounter data. 
    Response format:: 
    
        {'status':'SUCCESS', 
        'data': data,
        'encounter': encounter,
        'procedure_guid': procedure_guid, }
    
    Parameters:
        savedproc_guid
            an encounter, or saved procedure, id
        encounter
            encounter
        data
            encounter text data
    
    """
    response = {
        'status': 'SUCCESS',
        'data': data,
        'encounter': encounter,
        'procedure_guid': savedproc_guid,
        }
    return cjson.encode(response)