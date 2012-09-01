'''
Created on Aug 11, 2012

:author: Sana Development Team
:version: 2.0
'''
from django.dispatch import Signal

class EventSignal(Signal):
    """A generic message to pass to an EventSignalHandler holds content for   
       marking the event   
    """
    def __init__(self):
        Signal.__init__(self, providing_args=['event'])

class EventSignalHandler(object):
    """ Class based callback implementation for marking events. Creates and 
        saves a new instance of the model passed to the __init__ method.
    """
    def __init__(self, model):
        self.model = model
    
    def __call__(self, sender, **kwargs):
        data = sender.get('event')
        obj = self.model(**data)
        obj.save()

class CacheSignal(Signal):
    def __init__(self):
        Signal.__init__(self, providing_args=['uri','request', 'content'])

class FileCacheSignal(Signal):
    def __init__(self):
        Signal.__init__(self, providing_args=['uri','request', 'content'])
