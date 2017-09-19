# Create your models here.
import mimetypes, os

from django.db import models

__all__ = [
    "Client",
    "CrashReport"
]

class Client(models.Model):

    version = models.CharField(max_length=255)
    
    version_code = models.PositiveIntegerField()
                                
    app = models.FileField(upload_to='clients/', blank=True,)

    
class CrashReport(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    device = models.CharField(max_length=36, blank=True)
    report = models.FileField(upload_to='reports/', blank=True,)
    message = models.CharField(max_length=255, blank=True, default="None")
