# encoding: utf-8

from django.conf import settings
from django.db import models
from django.db.models import Q

from workon.utils import send_template_email, send_email

def notify(receiver, title, body, uid=None, email=None, email_sender=None, email_template=None, context_object=None):
    from .models import Notification
    if uid:
        # if uid send only if does not exists
        uid = uid[0:254]
        try:
            notification = Notification.objects.get(uid=uid)
            return None
        except Notification.DoesNotExist:
            pass

    is_email_sendable = False
    if email == True:
        #
        is_email_sendable = True

    notification = Notification(
        receiver=receiver,
        title=title,
        body=body,
        uid=uid,
        is_email_sendable=is_email_sendable,
        context_object=context_object,
        is_sent=True
    )

    if notification.is_email_sendable:

        kwargs = dict(
            subject=notification.title,
            sender=email_sender,
            receivers=[notification.receiver.email],
        )

        if email_template:
            kwargs.update(
                template=None,
                context={
                    'body': notification.body,
                    'context_object': notification.context_object,
                    'context_object': notification.context_object,
                },
            )
            send_template_email(**kwargs)
        else:
            kwargs.update(
                content=body,
            )
            send_email(**kwargs)
        notification.is_email_sent = True


    notification.save()


def notification_mark_as_read(receiver=None, context_object=None, notifications=None, notification=None, id=None, uid=None):

    from .models import Notification