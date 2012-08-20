'''
Created on Aug 11, 2012

:author: Sana Development Team
:version: 2.0
'''
from django.core.signals import request_finished, got_request_exception
from django.dispatch import Signal
from sana.core.models import RequestLog

class LogSignal(Signal):
    def __init__(self):
        Signal.__init__(self, providing_args=['uri','message', 'duration'])

class CacheSignal(Signal):
    def __init__(self):
        Signal.__init__(self, providing_args=['uri','request'])

class FileCacheSignal(Signal):
    def __init__(self):
        Signal.__init__(self, providing_args=['uri','request'])

def signal_logger(sender, **kwargs):
    uri=sender['uri']
    message=sender['message']
    duration=sender['duration']
    obj = RequestLog(uri=uri, message=message, duration=duration)
    obj.save()

def exception_logger(sender, **kwargs):
    uri=sender['uri']
    message=sender['message']
    duration=sender['duration']
    obj = RequestLog(uri=uri, message=message, duration=duration)
    obj.save()
