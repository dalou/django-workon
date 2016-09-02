# encoding: utf-8

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SecurityConfig(AppConfig):

    """
        'handlers': {
            ...

            'workon_security_disallowed_hosts': {
                'level': 'ERROR',
                'class': 'workon.contrib.security.handler.DisallowedHostHandler',
            }
        },
        'loggers': {
            ...

            'django.security.DisallowedHost': {
                'handlers': ['workon_security_disallowed_hosts'],
                'level': 'ERROR',
                'propagate': False,
            }
        },
    """
    name = 'workon.contrib.security'
    label = 'workon_security'
    verbose_name = _(u"Securité")

    def ready(self):
        from . import models

        # logger = logging.getLogger('django.security.DisallowedHost')
        # logger.setLevel(logging.ERROR)

        # handler = DisallowedHostHandler()
        # handler.setLevel(logging.ERROR)

        # logger.addHandler(handler)

        # # handlers 'spoof_logfile': {
        # #     'level': 'ERROR',
        # #     'class': 'logging.FileHandler',
        # #     'filename': '/path/to/spoofed_requests.log',
        # # },

        # # loggers 'django.security.DisallowedHost': {
        # #     'handlers': ['spoof_logfile'],
        # #     'level': 'ERROR',
        # #     'propagate': False,
        # # },