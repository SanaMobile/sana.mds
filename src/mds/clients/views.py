# Create your views here.
import cjson
import os

from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseNotFound

from mds.api.responses import JSONResponse

from .models import * 

FPATH = "/media/clients/app-android.apk"
VERSION = "2"

def version(request):
    client = current()
    message = client.version if client else VERSION
    return JSONResponse(cjson.encode({
        'status':'SUCCESS',
        'code':200, 
        'message': message}))

def download_version(request, version="latest"):
    if version == "latest":
        client = current()
    else:
        try:
            client = Client.objects.get(version__iexact=version)
        except:
            client = None
    # Return file download response or 404
    if client:
        filename = "sana-android-%s.apk" % client.version
        #os.path.basename(client.app.name)
        response = HttpResponse(
            client.app, 
            content_type="application/vnd.android.package-archive"
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
    else:
        response = HttpResponseNotFound("Version <strong>%s</strong> not available" % version)
    return response
    
def download_current(request):
    return download_version(request, version="latest")
