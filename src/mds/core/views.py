'''
Created on Aug 3, 2012

@author: Sana Development
'''
import cjson
import logging

from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate
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
         "version": mds.api.version, 
         "service": "REST"}
    """
    username = request.REQUEST.get('username', 'empty')
    password = request.REQUEST.get('password','empty')
    user = authenticate(username=username, password=password)
    if user is not None:
        return HttpResponse(cjson.encode( {
               'status':'SUCCESS',
               'code':200,
               'message': version()}))
    else:
        message = unicode('UNAUTHORIZED:Invalid credentials!')
        logging.warn(message)
        logging.debug(u'User' + username)
        return HttpResponse(cjson.encode({
                'status':'FAIL',
                'code':401, 
                'message': message}))
    

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
    data = []
    messages = cjson.decode(log.messages)
    for m in messages:
        try:
            m['message'] = cjson.decode(m['message'])
        except:
            pass
        
        data.append(m)
#           m['message']  = cjson.decode(m['message'])
#            data.append(m)
#        except:
            
            
    message = { 'message': data, 'uuid': uuid, }
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