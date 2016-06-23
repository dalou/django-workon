# coding: utf-8

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AuthConfig(AppConfig):
    name = 'workon.contrib.auth'
    label = 'workon_auth'
    verbose_name = _("Authentification")
