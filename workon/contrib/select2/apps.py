# coding: utf-8
'''
    Select2Config
'''
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class Select2Config(AppConfig):
    name = 'workon.contrib.select2'
    label = 'workon_select2'
    verbose_name = _(u"Select2 fork")