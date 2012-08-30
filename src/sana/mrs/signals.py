''' Dispatch signals to send messages with.

:author: Sana Development Team
:version: 2.0
'''
from sana.api.signals import EventSignal
from sana.core.models import RequestLog

def event_signalhandler(sender, **kwargs):
    data = sender.get('event')
    obj = RequestLog(**data)
    obj.save()

done_logging = EventSignal()
