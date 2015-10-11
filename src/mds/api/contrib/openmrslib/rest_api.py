'''
'''
import cjson

class RESTError(object):
    def __init__(self,response):
        error = response.pop('error') if response.has_key('error') else response
        self.code = error.get('code', None)
        self.message = error.get('message',None)
        self.details = error.get('details',None)
        
class RESTResult(object):
    def __init__(self,response,decoder=None):
        if isinstance(response,list):
            results = response
        else:
            results = response.pop('results', [])
        self.results = [decoder.decode(x) for x in results] if decoder else results

class RESTSession(object):
    def __init__(self,response):
        self.sessionId = response.pop('sessionId', None)
        self.authenticated = response.pop('authenticated', False)
        
class RESTResponse(object):
    def __init__(self, response, decoder=None):
        self._results = RESTResult(response.pop('results'),decoder=decoder) if response.has_key('results') else None
        self._error = RESTError(response.pop('error')) if response.has_key('error') else None
        self._session = RESTSession(response) if response.has_key('sessionId') else None
        self._instance = response

    @property
    def error(self):
        return bool(self._error is not None)

    @property
    def results(self):
        return self._results.results if self._results else []

    @property
    def session_id(self):
        return self._session.session_id if self._session else None
    
    @property
    def instance(self):
        return self._instance

def decode(response, result_decoder=None):
    ''' Takes a json encoded response body and returns a RESTResponse
        instance
        
        if 'result_decoder is specified, it will be used to decode 
        any 'results'.
    '''
    response_dict = cjson.decode(response)
    result = RESTResponse(response_dict, decoder=result_decoder)
    return result
