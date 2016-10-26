from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _


class TreeConfig(AppConfig):
    name = 'workon.contrib.tree'
    label = 'workon_tree'
    verbose_name = _("MPTT Tree")

    # def ready(self):
    #     post_migrate.connect(create_default_site, sender=self)
