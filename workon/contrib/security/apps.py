
from django.conf import settings
from django.utils.log import DEFAULT_LOGGING
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _

logging = settings.LOGGING
if not logging:
    logging = DEFAULT_LOGGING

if not logging.get('handlers'):
    logging['handlers'] = {}
if not logging.get('loggers'):
    logging['loggers'] = {}

logging['handlers']['workon_security_disallowed_hosts'] = {
    'level': 'ERROR',
    'class': 'workon.contrib.security.handler.DisallowedHostHandler',
    # 'filename': '/path/to/spoofed_requests.log',
}
logging['loggers']['django.security.DisallowedHost'] = {
    'handlers': ['workon_security_disallowed_hosts'],
    'level': 'ERROR',
    'propagate': False,
}

class SecurityConfig(AppConfig):
    name = 'workon.contrib.security'
    label = 'workon_security'
    verbose_name = _("Security")

    def ready(self):
        pass

        # handlers 'spoof_logfile': {
        #     'level': 'ERROR',
        #     'class': 'logging.FileHandler',
        #     'filename': '/path/to/spoofed_requests.log',
        # },

        # loggers 'django.security.DisallowedHost': {
        #     'handlers': ['spoof_logfile'],
        #     'level': 'ERROR',
        #     'propagate': False,
        # },