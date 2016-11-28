# encoding: utf-8

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class NotificationBase(models.Model):

    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True, db_index=True)
    sent_at = models.DateTimeField("Créé le", auto_now_add=True)

    receiver = models.ForeignKey('user.user', related_name='notifications', verbose_name=u"Receveur", null=True, blank=True)
    receiver_email = models.EmailField(u'Email receveur', null=True, blank=True)
    uid = models.CharField(u"UID", max_length=500, db_index=True, null=True, blank=True)
    type = models.CharField(u"Type", max_length=500, db_index=True, null=True, blank=True)

    subject = models.CharField(u"Sujet", max_length=500, null=True, blank=True)
    message = models.TextField(u"Body Message", null=True, blank=True)

    is_sent = models.BooleanField(u"Envoyee ?", default=False)
    is_read = models.BooleanField(u"Lu ?", default=False)

    is_email_sendable = models.BooleanField(u"A envoyer par email ?", default=False)
    is_email_sent = models.BooleanField(u"Envoyée par email ?", default=False)

    context_content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    context_object_id = models.PositiveIntegerField(db_index=True, null=True, blank=True)
    context_object = GenericForeignKey('context_content_type', 'context_object_id')
    context_object.short_description ="Objet"

    def save(self, **kwargs):
        if self.receiver and not self.receiver_email:
            self.receiver_email = self.receiver.email
        self.sent_at = timezone.now()
        super(NotificationBase, self).save(**kwargs)

    class Meta:
        abstract = True
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

notification_model = getattr(settings, 'WORKON', {}).get('notification', {}).get('model', 'workon_notification.notification')

if False:#notification_model == 'workon.notification':
    class Notification(NotificationBase):


        class Meta:
            db_table = "workon_notification_notification"
            verbose_name = 'Notification'
            verbose_name_plural = 'Notifications'
            ordering = ['-created_at']


# from django.conf import settings
# from django.contrib.contenttypes.models import ContentType
# from django import get_version
# from django.utils import timezone

# from distutils.version import StrictVersion

# if StrictVersion(get_version()) >= StrictVersion('1.8.0'):
#     from django.contrib.contenttypes.fields import GenericForeignKey
# else:
#     from django.contrib.contenttypes.generic import GenericForeignKey

# from django.db import models
# from django.core.exceptions import ImproperlyConfigured
# from django.utils.six import text_type
# from .utils import id2slug

# from .signals import notify

# from model_utils import Choices
# from workon.fields import JSONField

# from django.contrib.auth.models import Group


# # SOFT_DELETE = getattr(settings, 'NOTIFICATIONS_SOFT_DELETE', False)
# def is_soft_delete():
#     # TODO: SOFT_DELETE = getattr(settings, ...) doesn't work with "override_settings" decorator in unittest
#     #     But is_soft_delete is neither a very elegant way. Should try to find better approach
#     return getattr(settings, 'NOTIFICATIONS_SOFT_DELETE', False)


# def assert_soft_delete():
#     if not is_soft_delete():
#         msg = """To use 'deleted' field, please set 'NOTIFICATIONS_SOFT_DELETE'=True in settings.
#         Otherwise NotificationQuerySet.unread and NotificationQuerySet.read do NOT filter by 'deleted' field.
#         """
#         raise ImproperlyConfigured(msg)


# class NotificationQuerySet(models.query.QuerySet):

#     def unread(self, include_deleted=False):
#         """Return only unread items in the current queryset"""
#         if is_soft_delete() and not include_deleted:
#             return self.filter(unread=True, deleted=False)
#         else:
#             """ when SOFT_DELETE=False, developers are supposed NOT to touch 'deleted' field.
#             In this case, to improve query performance, don't filter by 'deleted' field
#             """
#             return self.filter(unread=True)

#     def read(self, include_deleted=False):
#         """Return only read items in the current queryset"""
#         if is_soft_delete() and not include_deleted:
#             return self.filter(unread=False, deleted=False)
#         else:
#             """ when SOFT_DELETE=False, developers are supposed NOT to touch 'deleted' field.
#             In this case, to improve query performance, don't filter by 'deleted' field
#             """
#             return self.filter(unread=False)

#     def mark_all_as_read(self, recipient=None):
#         """Mark as read any unread messages in the current queryset.

#         Optionally, filter these by recipient first.
#         """
#         # We want to filter out read ones, as later we will store
#         # the time they were marked as read.
#         qs = self.unread(True)
#         if recipient:
#             qs = qs.filter(recipient=recipient)

#         qs.update(unread=False)

#     def mark_all_as_unread(self, recipient=None):
#         """Mark as unread any read messages in the current queryset.

#         Optionally, filter these by recipient first.
#         """
#         qs = self.read(True)

#         if recipient:
#             qs = qs.filter(recipient=recipient)

#         qs.update(unread=True)

#     def deleted(self):
#         """Return only deleted items in the current queryset"""
#         assert_soft_delete()
#         return self.filter(deleted=True)

#     def active(self):
#         """Return only active(un-deleted) items in the current queryset"""
#         assert_soft_delete()
#         return self.filter(deleted=False)

#     def mark_all_as_deleted(self, recipient=None):
#         """Mark current queryset as deleted.
#         Optionally, filter by recipient first.
#         """
#         assert_soft_delete()
#         qs = self.active()
#         if recipient:
#             qs = qs.filter(recipient=recipient)

#         qs.update(deleted=True)

#     def mark_all_as_active(self, recipient=None):
#         """Mark current queryset as active(un-deleted).
#         Optionally, filter by recipient first.
#         """
#         assert_soft_delete()
#         qs = self.deleted()
#         if recipient:
#             qs = qs.filter(recipient=recipient)

#         qs.update(deleted=False)


# class Notification(models.Model):

#     LEVELS = Choices('success', 'info', 'warning', 'error')
#     level = models.CharField(choices=LEVELS, default=LEVELS.info, max_length=20)

#     recipient = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, related_name='notifications')
#     unread = models.BooleanField(default=True, blank=False)

#     actor_content_type = models.ForeignKey(ContentType, related_name='notify_actor')
#     actor_object_id = models.CharField(max_length=255)
#     actor = GenericForeignKey('actor_content_type', 'actor_object_id')

#     verb = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)

#     target_content_type = models.ForeignKey(ContentType, related_name='notify_target', blank=True, null=True)
#     target_object_id = models.CharField(max_length=255, blank=True, null=True)
#     target = GenericForeignKey('target_content_type', 'target_object_id')

#     action_object_content_type = models.ForeignKey(ContentType, blank=True, null=True,
#                                                    related_name='notify_action_object')
#     action_object_object_id = models.CharField(max_length=255, blank=True, null=True)
#     action_object = GenericForeignKey('action_object_content_type', 'action_object_object_id')

#     timestamp = models.DateTimeField(default=timezone.now)

#     public = models.BooleanField(default=True)
#     deleted = models.BooleanField(default=False)
#     emailed = models.BooleanField(default=False)

#     data = JSONField(blank=True, null=True)
#     objects = NotificationQuerySet.as_manager()

#     class Meta:
#         ordering = ('-timestamp', )
#         app_label = 'notifications'

#     def __unicode__(self):
#         ctx = {
#             'actor': self.actor,
#             'verb': self.verb,
#             'action_object': self.action_object,
#             'target': self.target,
#             'timesince': self.timesince()
#         }
#         if self.target:
#             if self.action_object:
#                 return u'%(actor)s %(verb)s %(action_object)s on %(target)s %(timesince)s ago' % ctx
#             return u'%(actor)s %(verb)s %(target)s %(timesince)s ago' % ctx
#         if self.action_object:
#             return u'%(actor)s %(verb)s %(action_object)s %(timesince)s ago' % ctx
#         return u'%(actor)s %(verb)s %(timesince)s ago' % ctx

#     def __str__(self):  # Adds support for Python 3
#         return self.__unicode__()

#     def timesince(self, now=None):
#         """
#         Shortcut for the ``django.utils.timesince.timesince`` function of the
#         current timestamp.
#         """
#         from django.utils.timesince import timesince as timesince_
#         return timesince_(self.timestamp, now)

#     @property
#     def slug(self):
#         return id2slug(self.id)

#     def mark_as_read(self):
#         if self.unread:
#             self.unread = False
#             self.save()

#     def mark_as_unread(self):
#         if not self.unread:
#             self.unread = True
#             self.save()

# # 'NOTIFY_USE_JSONFIELD' is for backward compatibility
# # As app name is 'notifications', let's use 'NOTIFICATIONS' consistently from now
# EXTRA_DATA = getattr(settings, 'NOTIFY_USE_JSONFIELD', None)
# if EXTRA_DATA is None:
#     EXTRA_DATA = getattr(settings, 'NOTIFICATIONS_USE_JSONFIELD', False)


# def notify_handler(verb, **kwargs):
#     """
#     Handler function to create Notification instance upon action signal call.
#     """

#     # Pull the options out of kwargs
#     kwargs.pop('signal', None)
#     recipient = kwargs.pop('recipient')
#     actor = kwargs.pop('sender')
#     optional_objs = [
#         (kwargs.pop(opt, None), opt)
#         for opt in ('target', 'action_object')
#     ]
#     public = bool(kwargs.pop('public', True))
#     description = kwargs.pop('description', None)
#     timestamp = kwargs.pop('timestamp', timezone.now())
#     level = kwargs.pop('level', Notification.LEVELS.info)

#     # Check if User or Group
#     if isinstance(recipient, Group):
#         recipients = recipient.user_set.all()
#     else:
#         recipients = [recipient]

#     for recipient in recipients:
#         newnotify = Notification(
#             recipient=recipient,
#             actor_content_type=ContentType.objects.get_for_model(actor),
#             actor_object_id=actor.pk,
#             verb=text_type(verb),
#             public=public,
#             description=description,
#             timestamp=timestamp,
#             level=level,
#         )

#         # Set optional objects
#         for obj, opt in optional_objs:
#             if obj is not None:
#                 setattr(newnotify, '%s_object_id' % opt, obj.pk)
#                 setattr(newnotify, '%s_content_type' % opt,
#                         ContentType.objects.get_for_model(obj))

#         if len(kwargs) and EXTRA_DATA:
#             newnotify.data = kwargs

#         newnotify.save()


# # connect the signal
# notify.connect(notify_handler, dispatch_uid='notifications.models.notification')