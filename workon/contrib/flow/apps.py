# coding: utf-8
'''
    AppConfig
'''
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _



class FlowConfig(AppConfig):
    name = 'workon.contrib.flow'
    label = 'workon.flow'
    verbose_name = _("Real time websocket per user backend")

