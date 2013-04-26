'''
Created on Aug 3, 2012

@author: Sana Development
'''
import cjson
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext 

from mds.api import version
from mds.api.responses import JSONResponse
from .models import Event

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
    
    

def _list(request,*args,**kwargs):
    query = dict(request.GET.items())
    start = int(query.get('start', 1))
    limit = int(query.get('limit', 20))
    objects = Event.objects.all().filter().order_by('-created')
    paginator = Paginator(objects, limit, allow_empty_first_page=True)
    objs = []
    for p in paginator.page(start).object_list.all():
        obj = p.to_python()
        m = obj.pop('message')
        try:
            obj['message'] = cjson.decode(m,True)
        except:
            obj['message'] = m
        objs.append(obj)
    data = {'objects': objs,
            'limit': limit,
            'start': start,
            "rate": int(query.get('refresh', 5)),
            'range': range(1, paginator.num_pages + 1),
            "version": settings.API_VERSION }
    return data

def log_index(request,*args,**kwargs):
    data = _list(request)
    return render_to_response('logging/index.html', RequestContext(request,data))

def log_list(request):
    data = _list(request)
    return render_to_response('logging/list.html', RequestContext(request,data))

def log_report(request):
    post = dict(request.POST.items())
    selected = []
    for k,v in post.items():
        if v:
            selected.append(k)
    objects = Event.objects.all().filter(uuid__in=selected)
    return JSONResponse(objects)

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

def log(request,*args,**kwargs):
    query = dict(request.GET.items())
    page = int(query.get('page', 1))
    page_size = int(query.get('page_size', 20))
    
    data = {'object_list': {},
            'page_range': range(0, 1),
            'page_size': page_size,
            'page': page,
            "rate": int(query.get('refresh', 5)) }
    return render_to_response('logging/index.html', RequestContext(request,data))

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