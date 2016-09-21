# Create your views here.
from django.conf import settings
from django.http import HttpResponse

from mds.api.responses import JSONResponse, json_succeed, json_fail, json_unauthorized

from .forms import CrashReportForm
from .models import Client, CrashReport

FPATH = "/media/clients/app-android.apk"
VERSION = "2"

def version(request):
    authenticated = getattr(request, "authenticated", False)
    if not authenticated:
        return json_unauthorized(["Invalid credentials",])
    obj = Client.objects.order_by('-version_code').first()
    if not obj:
        return json_succeed({ "version": -1 })
    return json_succeed({ "version": obj.version_code })
        
def download_latest(request):
    authenticated = getattr(request, "authenticated", False)
    if not authenticated:
        return json_unauthorized(["Invalid credentials",])
    obj = Client.objects.order_by('-version_code').first()
    if not obj:
        response = HttpResponse(data,
            content_type='application/vnd.android.package-archive')
        response['Content-Disposition'] = 'attachment; filename=%s' % fname
        response['Content-Length'] = 0
        response.status_code = 200
        return response
    data = obj.app
    fname = data.name.split('/')[-1]
    response = HttpResponse(data,
            content_type='application/vnd.android.package-archive')
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    response['Content-Length'] = data.size
    response.status_code = 200
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
