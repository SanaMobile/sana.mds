# Create your models here.
import mimetypes, os

from django.db import models


class Client(models.Model):

    version = models.CharField(max_length=255)
                                
    app = models.FileField(upload_to='clients/', blank=True,)

    def __unicode__(self):
        return self.version

def current(platform="android"):
    return Client.objects.order_by("-version").first()
    
def current_version_info(platform="android"):
    client = current(platform=platform)
    return client.version if client else None
