# encoding: utf-8

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import six
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model

from workon.utils import send_email

def notify(subject, message, receivers, uid=None, type=None, context_object=None, email=None, email_sender=None, email_grouped=False):
    from .models import Notification
    User = get_user_model()

    is_email_sendable = False

    if isinstance(receivers, six.string_types):
        receivers = [ r.strip().lower() for r in receivers.split(',') ]

    elif isinstance(receivers, list):
        receivers = receivers

    elif isinstance(receivers, QuerySet):
        receivers = receivers

    else:
        receivers = [receivers]

    notifications = []
    for receiver in receivers:
        if uid:
            # if uid send only if does not exists
            uid = uid[0:500]
            try:
                if isinstance(receiver, six.string_types):
                    notification = Notification.objects.get(receiver_email=receiver.strip().lower(), uid=uid)

                if isinstance(receiver, Notification._meta.fields['receiver'].model):
                    notification = Notification.objects.get(receiver=receiver, uid=uid)

                return None

            except Notification.DoesNotExist:
                pass

        if email is not None:
            is_email_sendable = True

        notification = Notification(
            subject=subject,
            message=message,
            uid=uid,
            type=type,
            is_email_sendable=is_email_sendable,
            context_object=context_object,
            is_sent=True,
            is_email_sent=True
        )

        if isinstance(receiver, six.string_types):
            email = receiver.strip().lower()
            try:
                receiver = User.objects.get(email=email)
            except User.DoesNotExist:
                receiver = None
            notification.receiver_email = email
            notification.receiver = receiver
            notification.save()
            notifications.append(notification)

        elif isinstance(receiver, User):
            notification.receiver = receiver
            notification.receiver_email = receiver.email.strip().lower()
            notification.save()
            notifications.append(notification)



    if is_email_sendable and notifications:

        if email_grouped:

            notification = notifications[0]
            notify_send_email(
                notification=notification,
                email=email,
                sender=email_sender,
                receivers=[n.receiver_email for n in notifications],
            )
            for notification in notifications:
                notification.is_email_sent = True
                notification.save()

        else:

            for notification in notifications:

                notify_send_email(
                    notification=notification,
                    email=email,
                    sender=email_sender,
                    receivers=[notification.receiver_email],
                )
                notification.is_email_sent = True
                notification.save()
    return notifications

def notify_send_email(notification, email, sender, receivers):
    kwargs = dict(
        subject=notification.subject,
        sender=sender if sender else settings.DEFAULT_FROM_EMAIL,
        receivers=receivers,
        content=notification.message
    )

    if isinstance(email, dict):

        template = email.pop('template', None)
        kwargs.update(email)

        if template:
            context = {
                'notification': notification,
                'receivers': receivers,
            }
            context.update(kwargs.pop('context', {}))
            send_email(template=template, context = context, **kwargs)
        else:
            send_email(content=notification.message, **kwargs)

    elif email == True:
        kwargs.update(
            message=message,
        )
        if isinstance(email, dict):
            kwargs.update(email)
            kwargs['message'] = kwargs.get('content', message)

        send_email(**kwargs)



def notification_mark_as_read(receiver=None, context_object=None, notifications=None, notification=None, id=None, uid=None):

    from .models import Notification