''' The base HTTP openers for OpenMRS

:author: Sana Development Team
:version: 2.0
'''
import urllib
import cookielib
import urllib2
import cjson

from sana.api.contrib import handlers

__all__ = ['OpenMRSOpener', 'response_reader', 'rest_reader']

def response_reader(response):
    """ Default response handler. Returns
    """
    code = response.status_code
    message = response.read()
    return code, message
    
def rest_reader(response, all_unicode=False):
    code = response.status_code
    msg = cjson.decode(response.read(), all_unicode=all_unicode)
    if "error" in msg.keys():
        error_content = msg["error"]
        message = error_content["code"]
        return code, message
    else:
        message = msg["results"]
    return code, message
        
    
def session_reader(response, all_unicode=False):
    code = response.status_code
    msg = cjson.decode(response.read(), all_unicode=all_unicode)
    if "error" in msg.keys():
        error_content = msg["error"]
        message = error_content["code"]
        return code, message
    else:
        message = msg
    return code, message
    

def defresource_reader(response, all_unicode=False):
    pass

def fullresource_reader(response, all_unicode=False):
    pass


class OpenMRSOpener(object):
    def __init__(self, username, password, openmrs_host):
        """Called when a new OpenMRS object is initialized.
            
        Parameters:
            username
                A valid user name for authoriztion
            password
                A valid user password for authorization
            url
                The OpenMRS host root url including port.
        """
        self.username = username
        self.password = password
        self.host = openmrs_host
        self.cookies = cookielib.CookieJar()
        
        try:
            self._build_opener(self.host, username, password)
        except Exception:
            self.opener = None
    
    def _build_opener(self, url, username, password):
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, username, password)
        auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        self.opener = urllib2.build_opener(
                auth_handler,
                urllib2.HTTPCookieProcessor(self.cookies),
                handlers.MultipartPostHandler)
        
    
    def get_path(self, key):
        """ Returns path string by key value-e.g. create_<key>, read_<key>, 
            etc.
        """
        return getattr(self.__class__, key, "")
    
    def buildurl(self,path,**query):
        if query:
            qstring = urllib.urlencode(query)
            return '{0}{1}?{2}'.format(self.host, path, qstring)
        else:
            return '{0}{1}'.format(self.host, path)
    
    def open(self, url, username=None, password=None, **kwargs):
        if not self.opener:
            self._build_opener(self.host, username, password)
        # This always seemed really redundant can we remove
        cookies = cookielib.CookieJar()
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, username, password)
        auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(auth_handler,
                                      urllib2.HTTPCookieProcessor(cookies),
                                      handlers.MultipartPostHandler)
        urllib2.install_opener(opener)
        return self.opener.open(url, kwargs)
    
    def create(self, path, response_handler=None, **kwargs):
        """ Sends an Http POST for object creation. Returns the response object
            for post processing.
        """
        username=kwargs.get("username","") if kwargs else ""
        password=kwargs.get("password","") if kwargs else ""
        response = self.open(self.buildurl(path), kwargs, username=username, 
                         password=password)
        if response_handler:
            return response_handler(response)
        else:
            return response
    
    def read(self, path, response_handler=None, **query):
        """ Sends an Http GET request for object retrieval. If passed a query,
        it will be encoded and appended to the path
        """
        username=query.get("username","")
        password=query.get("password","")  
        response = self.open(self.buildurl(path, query), username=username, 
                         password=password)
        if response_handler:
            return response_handler(response)
        else:
            return response
            
    def update(self, path, **kwargs):
        """ Sends an Http PUT for object updates.
        """
        return self.create(path, kwargs)
    
    def delete(self, path, **kwargs):
        """ Sends an Http DELETE for object removal.
        """
        #TODO
        pass
    
    def create_subject(self, response_handler=rest_reader, **kwargs):
        """ Wrapper for self.create for a subject. Returns the unread 
            HttpResponse
        """
        path = self.get_path("_create_subject")
        return self.create(path, response_handler=response_handler, **kwargs)
        
    def read_subject(self, uuid=None, response_handler=rest_reader, **query):
        """ Wrapper for self.read. Passing the uuid will append it to the 
            subject url registered to the class. The response_handler
            should be a callable to execute on the result of the self.read 
            call if desired
        """
        path = self.get_path("_read_subject").format(uuid=uuid)
        return self.read(path, response_handler=response_handler, **query)
        
    def create_encounter(self, response_handler=rest_reader, **kwargs):
        """ Wrapper for self.create for an encounter. Returns the unread 
            HttpResponse.
        """
        path = self.get_path("_create_encounter")
        return self.create(path, response_handler=response_handler, **kwargs)
    
    def read_encounter(self, uuid="", response_handler=rest_reader):
        """ Wrapper for self.read. Passing the uuid will append it to the 
            subject url registered to the class. The response_handler
            should be a callable to execute on the result of the self.read 
            call if desired.
        """
        path = self.get_path("_read_encounter").format(uuid=uuid)
        return self.read(path, response_handler=response_handler)
    
    
    