''' The OpenMRS request handlers and utilities'''

import urllib
import cookielib
import logging
import urllib2
import cjson
import time
import sys, traceback

from sana.api.contrib import handlers

CURRENT_VERSION=1.9

def get_opener(version=CURRENT_VERSION):
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
                The OpenMRS host root url having the form::
                
                    http:<ip or hostname>[:8080 | 80]/openmrs/
                
                and defined in the settings.py module
        """
        self.username = username
        self.password = password
        self.host = openmrs_host
        self.cookies = cookielib.CookieJar()

        try:
            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(None, self.url, self.username, self.password)
            auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            self.opener = urllib2.build_opener(
                auth_handler,
                urllib2.HTTPCookieProcessor(self.cookies),
                handlers.MultipartPostHandler)
        except Exception, e:
            print "Couldn't initialize openMRS interface, exception: " + str(e)
    
    def buildurl(self,path,**query):
        if query:
            qstring = urllib.urlencode(query)
            return '{0}{1}?{2}'.format(self.host, path, qstring)
        else:
            return '{0}{1}?{2}'.format(self.host, path)
    
    def open(self, url,**data):
        return self.opener.open(url, data)
    
    def post(self, path, **data):
        return self.open(self.buildurl(path), data).read()
        
    def get(self, path, **data):
        return self.open(self.buildurl(path, data))
        
        