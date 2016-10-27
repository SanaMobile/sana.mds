# Create your views here.
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, StreamingHttpResponse

from mds.api.responses import JSONResponse, json_succeed, json_fail, json_unauthorized
from mds.api.responses import unauthorized, succeed

from .forms import CrashReportForm
from .models import Client, CrashReport

VERSION = "2"

def version(request):
    authenticated = getattr(request, "authenticated", False)
    if not authenticated:
        result = []
        result.append("Invalid credentials")
        return json_unauthorized(result)
    qs = Client.objects.order_by('-version_code')
    if not qs:
        return json_succeed({ "version": -1 })
    obj = qs.first()
    f = obj.app
    size = f.size
    return json_succeed({ 
        "version": obj.version_code, 
        "url": f.url,
        "name" : obj.version },
        size=size )
        
def invalid_file(request):
    response = HttpResponse(
        content_type='application/vnd.android.package-archive')
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    response['Content-Length'] = 0
    response.status_code = 400
    return response
    
def download_latest(request):
    authenticated = getattr(request, "authenticated", False)
    if not authenticated:
        return json_unauthorized(["Invalid credentials",])
    obj = Client.objects.order_by('-version_code').first()
    if not obj:
        return invalid_file(request)
    data = obj.app
    fname = data.name.split('/')[-1]
    response = HttpResponse(data,
            content_type='application/vnd.android.package-archive')
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    response['Content-Length'] = data.size
    response.status_code = 200
    return response
    
def download_latest_x_sendfile(request, filename):
    obj = Client.objects.order_by('-version_code').first()
    if not obj:
        return invalid_file(request)
    data = obj.app
    fname = data.name.split('/')[-1]
    response = HttpResponse(content_type='application/vnd.android.package-archive')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(fname)
    response['X-Sendfile'] = data.name
    response['Content-Length'] = data.size
    return response
    
def submit_crash(request):
    authenticated = getattr(request, "authenticated", False)
    if not authenticated:
        return json_unauthorized(["Invalid credentials",])
    if request.method == 'POST':
        form = CrashReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return json_succeed({ "created": form.instance.created })
        else:
            return json_fail([], code=400, errors=form.errors)
    else:
        return json_fail([], code=400)
