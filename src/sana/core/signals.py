'''
Created on Aug 11, 2012

:author: Sana Development Team
:version: 2.0
'''
from django.core.signals import request_finished, got_request_exception
from django.core.urlresolvers import resolve

from django.dispatch import receiver, Signal
from sana.core.models import RequestLog

done_logging = Signal(providing_args=['log'])

class LogSignal(Signal):
    def __init__(self):
        Signal.__init__(self, providing_args=['log'])

def signal_logger(sender, **kwargs):
    log = sender['log']
    # reroute it to the correct sub domain of core table here
    obj = RequestLog.__init__(log)
    obj.save()

def exception_logger(sender, **kwargs):
    log = sender['log']
    # reroute it to the correct sub domain of core table here
    obj = RequestLog.__init__(log)
    obj.save()


