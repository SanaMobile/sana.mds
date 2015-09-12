""" Utilities for sending email messages through SMTP.

:author: Sana Development Team
:version: 2.0
"""
import urllib
import logging

from django.conf import settings
from django.core.mail import send_mail

__all__ = ["send_review_notification",]

#TODO These should be saved as settings or a global config table
link = "https://%s/mds/web/form/surgeon/review/%s/"
#mobile_link = "https://%s/mds/core/mobile/%s/%s/"

def send_review_notification(instance,addresses,subject,
    review_host=settings.REVIEW_HOSTNAME, 
    replyTo=settings.SMTP_REPLYTO,
    template=settings.REVIEW_POST_TEMPLATE,
    auth_user=settings.EMAIL_HOST_USER,
    auth_password=settings.EMAIL_HOST_PASSWORD):
    """ Formats and sends and email message which include a url for reviewing
        an uploaded encounter.
    """
    try:
        url = link % (
            review_host,
            instance.uuid
        )
        logging.debug("review link %s" % url)
        #urlencodred = urllib.urlencode(url)
        #print urlencoded)
        message = template % (url)
        logging.debug("Review message:\n %s" % message)
        send_mail(subject, message, settings.SMTP_REPLYTO,addresses, 
                    fail_silently=False,
                    auth_user=auth_user, 
                    auth_password=auth_password)
        for address in addresses:
            print address
            logging.info("Review notification sent successfully to %s" % address)
        result = True
    except:
        logging.error("Review notification send failed!")
        result = False
    return result
