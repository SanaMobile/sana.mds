'''
Created on Aug 3, 2012

@author: ewinkler
'''
import cjson
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from sana.api import version
from sana.core.models import Event

def home(request):
    """Top level url
    
    Displays ::
        {"path": HttpRequest.path, 
         "host": HttpRequest.get_host(), 
         "version": sana.api.version, 
         "service": "REST"}
    """
    return HttpResponse(cjson.encode({'service':'REST',
                         'version': version(),
                         'path': request.path,
                         'host':request.get_host()
                         }))
    
    
from django.shortcuts import render_to_response
from django.template import RequestContext 
from sana.api.responses import render_json_response
def _list(request,*args,**kwargs):
    query = dict(request.GET.items())
    start = int(query.get('start', 1))
    limit = int(query.get('limit', 20))
    objects = Event.objects.all().filter().order_by('-created')
    paginator = Paginator(objects, limit, allow_empty_first_page=True)
    objs = []
    for p in paginator.page(start).object_list.all():
        obj = p.get_representation(rep = 'full')
        m = obj.pop('message')
        try:
            obj['message'] = cjson.decode(m,True)
            print 'decoded'
        except:
            obj['message'] = m
        objs.append(obj)
    data = {'objects': objs,
            'limit': limit,
            'start': start,
            "rate": int(query.get('refresh', 5)),
            'range': range(1, paginator.num_pages + 1) }
    return data

def log_index(request,*args,**kwargs):
    data = _list(request)
    return render_to_response('logging/index.html', RequestContext(request,data))

def log_list(request):
    data = _list(request)
    return render_to_response('logging/list.html', RequestContext(request,data))


def log_detail(request, uuid):
    log = Event.objects.get(uuid=uuid)
    try:
        print type(log.messages)
        
        for x in log.messages:
            x['message'] = cjson.decode(x)
            print x['message']
    except:
        data = log.message
    message = {'id': uuid, 'data': data }
    return HttpResponse(cjson.encode(message))

if __name__ == 'main':
    data = {"data": [
               {'line_number': 44, 
                'level_number': 10, 
                'delta': '0.000s', 
                'timestamp': 1344815434.9979069, 
                'level_name': 'DEBUG', 
                'function_name': 'execute', 
                'message': u'(0.002) SELECT \"core_concept\".\"id\", \"core_concept\".\"uuid\", \"core_concept\".\"created\", \"core_concept\".\"modified\", \"core_concept\".\"name\", \"core_concept\".\"display_name\", \"core_concept\".\"description\", \"core_concept\".\"conceptclass\", \"core_concept\".\"datatype\", \"core_concept\".\"mimetype\", \"core_concept\".\"constraint\" FROM \"core_concept\"; args=()', 
                'module': 'util', 
                'filename': 'util.py'}], 
            "id": "2bbeb878-33f1-4590-9237-e41b151fa553"}