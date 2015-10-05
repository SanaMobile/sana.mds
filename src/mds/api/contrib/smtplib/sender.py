""" Utilities for sending email messages through SMTP.

:author: Sana Development Team
:version: 2.0
"""
import urllib
import logging

from django.conf import settings
from django.core.mail import send_mail, mail_admins

__all__ = ["send_review_notification",]

def send_review_notification(instance,addresses,subject,
    review_host=settings.REVIEW_HOSTNAME, 
    replyTo=settings.SMTP_REPLYTO,
    template=settings.REVIEW_POST_TEMPLATE,
    review_link=settings.REVIEW_URL_TEMPLATE,
    auth_user=settings.EMAIL_HOST_USER,
    auth_password=settings.EMAIL_HOST_PASSWORD):
    """ Formats and sends and email message which include a url for reviewing
        an uploaded encounter.
    """
    result = True
    try:
        url = review_link.format(
            review_host=review_host,
            uuid=instance.uuid
            )
        message = template.format(url=url)
        # Send one at a time here
        for address in addresses:
            try:
                send_mail(subject, message, settings.SMTP_REPLYTO,
                    [address], 
                    fail_silently=False,
                    auth_user=auth_user, 
                    auth_password=auth_password)
                logging.info("Notification sent successfully %s" % address)
            except:
                fail_msg = "Notification send failed! {address}".format(address=address)
                logging.warn(fail_msg)
                result = False
                mail_admins("Server Error", fail_message, fail_silently=True)
    except:
        logging.error("Error formatting notification message!")
        result = False
    return result
