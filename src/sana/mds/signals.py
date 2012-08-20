'''
Created on Aug 11, 2012

:author: Sana Development Team
:version: 2.0
'''
from django.core.signals import request_finished, got_request_exception, request_started
from django.dispatch import receiver, Signal
from sana.mds.models import RequestLog

def signal_logger(sender, **kwargs):
    obj = RequestLog(kwargs['signal'])
    obj.save()

def exception_logger(sender, **kwargs):
    print __name__ + '.exception_logger::', kwargs['signal'].providing_args

done_logging = Signal(providing_args=['uri','message', 'duration'])
#done_logging.connect(signal_logger)
