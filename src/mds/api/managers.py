from django.db import models

__all__ = [
    'APIManager',
    ]

class APIManager(models.Manager):
    def get_queryset(self):
        return super(APIManager, self).get_queryset().filter(voided=False)
        
    def modified(self, modified):
        return self.get_queryset().filter(modified__gt=modified)
        
    def voided(self):
        return super(APIManager, self).get_queryset().filter(voided=True)
