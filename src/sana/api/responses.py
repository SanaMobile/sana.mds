'''
Created on Aug 11, 2012

:author: Sana Development Team
:version: 2.0
'''
from django.http import HttpResponse


def render_json_response(data):
    return JSONResponse(data)

class JSONResponse(HttpResponse):
    """ Extension of HttpResponse with X-JSON header and the mimetype set to 
        application/json and charset to settings.DEFAULT_CHARSET
        
        Parameters:
            data
                message content
    """
    def __init__(self, data):
        HttpResponse.__init__(self, data, mimetype="application/json")
        self['X-JSON'] = data

def fail(data):
    ''' Fail response as a python dict with data '''
    response = {'status': 'FAILURE',
                'message': data}
    return response

def succeed(data):
    ''' Success response as a python dict with data '''
    response = {'status': 'SUCCESS',
                'message': data}
    return response

if __name__ == 'main':
    import cjson
    data = cjson.encode({'a':'1'})
    js = JSONResponse(data)
    print js._headers
    
    