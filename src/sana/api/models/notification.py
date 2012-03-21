"""
Notifications for the Sana data engine.

:Authors: Sana dev team
:Version: 1.1
"""
import cjson

from django.db import models

class Notification(models.Model):
    """ A message to be sent
    """
    class Meta:
        app_label = 'mrs'

    # some identifier that tells us which client it is (phone #?)
    client = models.CharField(max_length=512)
    patient_id = models.CharField(max_length=512)
    procedure_id = models.CharField(max_length=512)

    message = models.TextField()
    delivered = models.BooleanField()

    def to_json(self):
        return cjson.encode({
            'phoneId': self.client,
            'message': self.message,
            'procedureId': self.procedure_id,
            'patientId': self.patient_id
            })
        
    def flush(self):
        """ Removes the message text """
        self.message = ''
        self.save()