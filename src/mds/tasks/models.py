from django.db import models

from mds.core.models import Subject, Observer, Procedure

class Status(models.Model):
    
    current = models.CharField(max_length=128)

class Task(models.Model):
    assigned_to = models.ForeignKey(Observer)
    status = models.ForeignKey(Status)
    
    due_on = models.DateTimeField()
    """ updated on modification """
    
    created = models.DateTimeField(auto_now_add=True)
    """ When the object was created """
    
    modified = models.DateTimeField(auto_now=True)
    """ updated on modification """
    
class Subject_Visit(Task):
    subject = models.ForeignKey(Subject)
    procedure = models.ForeignKey(Procedure)