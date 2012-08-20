'''
Created on Aug 3, 2012

@author: ewinkler
'''
import cjson
from django.http import HttpResponse
from sana.api import version

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
       