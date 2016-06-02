from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _


class NotificationConfig(AppConfig):
    name = 'workon.contrib.notification'
    verbose_name = _("Notifications")

    # def ready(self):
    #     post_migrate.connect(create_default_site, sender=self)