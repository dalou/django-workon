
from django.conf import settings
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _


class SecurityConfig(AppConfig):
    name = 'workon.contrib.security'
    label = 'workon_security'
    verbose_name = _("Security")

    def ready(self):
        print settings.LOGGING

        # 'spoof_logfile': {
        #     'level': 'ERROR',
        #     'class': 'logging.FileHandler',
        #     'filename': '/path/to/spoofed_requests.log',
        # },

        # 'django.security.DisallowedHost': {
        #     'handlers': ['spoof_logfile'],
        #     'level': 'ERROR',
        #     'propagate': False,
        # },