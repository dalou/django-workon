# encoding: utf-8

from django.conf import settings
from django.db import models
from django.db.models import Q

from workon.utils import send_template_email, send_email

def notify(receiver, title, body, uid=None, email=None, template_email=None, context_object=None):
    from .models import Notification
    if uid:
        # if uid send only if does not exists
        uid = uid[0:254]
        try:
            notification = Notification.objects.get(receiver=receiver, uid=uid)
            return None
        except Notification.DoesNotExist:
            pass

    is_email_sendable = False
    if email is not None or template_email is not None:
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
    notification.save()

    if notification.is_email_sendable:

        kwargs = dict(
            subject=notification.title,
            sender=settings.DEFAULT_FROM_EMAIL,
            receivers=[notification.receiver.email],
        )

        if isinstance(template_email, str) or isinstance(template_email, dict):
            kwargs.update(
                template=template_email if isinstance(template_email, str) else None,
                context={
                    'receiver': receiver,
                    'title': notification.title,
                    'body': notification.body,
                    'context_object': notification.context_object,
                },
            )
            if isinstance(template_email, dict):
                kwargs.update(template_email)
            send_template_email(**kwargs)
        else:
            kwargs.update(
                body=body,
            )
            if isinstance(email, dict):
                kwargs.update(email)
                kwargs['body'] = kwargs.get('content', body)

            send_email(**kwargs)
        notification.is_email_sent = True
        notification.save()




def notification_mark_as_read(receiver=None, context_object=None, notifications=None, notification=None, id=None, uid=None):

    from .models import Notification