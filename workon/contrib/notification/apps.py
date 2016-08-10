from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _


class NotificationConfig(AppConfig):
    name = 'workon.contrib.notification'
    label = 'workon_notification'
    verbose_name = _("Notifications")

    def ready(self):
        from .utils import notification_mark_as_read, notify

