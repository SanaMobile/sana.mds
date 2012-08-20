'''
Created on Aug 11, 2012

:author: Sana Development Team
:version: 2.0
'''
try:
    import json as simplejson
except ImportError, e:
    import simplejson
    
import logging
import urllib

from django.conf import settings
from sana.api.contrib.smslib.messages import format_sms

def send_kannel_notification(n, phoneId):
    return KannelOpener().open(n, phoneId)

class KannelOpener:
    
    def __init__(self):
        pass
    
    def open(self, n, phoneId):
        """Sends a notification to a phone as one or more sms messages through a
        Kannel SMS gateway.
        
        Parameters:    
            n
                The message body
            phoneId
                The recipient
        """
        result = False
        try:
            messages = format_sms(n)
            for message in messages:
                params = urllib.urlencode({
                        'username': settings.KANNEL_USER,
                        'password': settings.KANNEL_PASSWORD,
                        'to': phoneId,
                        'text': message
                        })
    
                logging.info("Sending kannel notification %s to %s" %
                             (message, phoneId))
                response = urllib.urlopen(settings.KANNEL_URI % params).read()
                logging.info("Kannel response: %s" % response)
                result = True
        except Exception, e:
            logging.error("Couldn't submit Kannel notification for %s: %s" 
                          % (phoneId, e))
        return result