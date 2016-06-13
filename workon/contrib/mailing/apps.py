from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SelectionConfig(AppConfig):
    name = 'workon.contrib.mailing'
    label = 'workon.mailing'
    verbose_name = _("Mailing")

    # def ready(self):
    #     post_migrate.connect(create_default_site, sender=self)
