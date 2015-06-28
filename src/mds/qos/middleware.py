'''

'''
import datetime

QOS_SOURCE = 'source'
QOS_TARGET = 'target'
QOS_SENT = 'sent'
QOS_RECEIVED = 'received'
QOS_SEND_COUNT = 'send_count'
QOS_EVENT_START = 'event_start'
QOS_EVENT_COMPLETE = 'event_complete'
QOS_REQUEST_COMPLETE = 'request_complete'
QOS_HEADER_PREFIX = 'HTTP_QOS_'

def django_header_key(name):
    return QOS_HEADER_PREFIX + name.upper()
    
QOS_HEADERS = [
    QOS_SOURCE,
    QOS_TARGET,
    QOS_SENT,
    QOS_RECEIVED,
    QOS_SEND_COUNT,
    QOS_EVENT_START,
    QOS_EVENT_COMPLETE,
    QOS_REQUEST_COMPLETE,
]

DJANGO_QOS_HEADERS = []

class QOSMiddleware(object):
    def process_request(self,request):
        meta = request.META
        qos = {}
        for key in QOS_HEADERS:
            header = django_header_key(
            qos[key] = meta.get(header,None)
        # set the 'send_count' to 1 if not specified
        if not qos[QOS_SEND_COUNT]:
            qos[QOS_SEND_COUNT] = 1
        # fill in some fields that won't get sent in headers
        qos[QOS_RECEIVED] = datetime.datetime.now()
        qos[QOS_TARGET] = request.path
        setattr(request,'qos',qos)
        return None
        
    def process_response(self,request,response):
        if request.hasttr('qos'):
            qos[QOS_REQUEST_COMPLETE] = datetime.datetime.now()
            # do something
            pass
         return response

