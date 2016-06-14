from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _


class TrackingConfig(AppConfig):
    name = 'workon.contrib.tracking'
    label = 'workon_tracking'
    verbose_name = _("Tracking fields")

    # def ready(self):
    #     post_migrate.connect(create_default_site, sender=self)
