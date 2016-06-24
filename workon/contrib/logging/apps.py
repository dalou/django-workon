
from django.conf import settings
from django.utils.log import DEFAULT_LOGGING
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _

# logging = settings.LOGGING
# if not logging:
#     logging = DEFAULT_LOGGING

# if not logging.get('handlers'):
#     logging['handlers'] = {}
# if not logging.get('loggers'):
#     logging['loggers'] = {}

# logging['handlers']['workon_security_disallowed_hosts'] = {
#     'level': 'ERROR',
#     'class': 'workon.contrib.security.handler.DisallowedHostHandler',
#     # 'filename': '/path/to/spoofed_requests.log',
# }
# logging['loggers']['django.security.DisallowedHost'] = {
#     'handlers': ['workon_security_disallowed_hosts'],
#     'level': 'ERROR',
#     'propagate': False,
# }
# settings.LOGGING = logging

class LoggingConfig(AppConfig):
    name = 'workon.contrib.logging'
    label = 'workon_logging'
    verbose_name = _("Logging")

    def ready(self):
        pass

        # handlers 'spoof_lo