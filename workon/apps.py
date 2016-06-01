import os

import email as original_email
from django.apps import AppConfig
from django import get_version

from django.conf import settings
from django.contrib import admin
from django.contrib.admin import options
from django.db import models

class WorkonConfig(AppConfig):

    name = 'workon'

    def __init__(self, app_name, app_module):
        super(WorkonConfig, self).__init__(app_name, app_module)

    def ready(self):
        from . import models
        super(WorkonConfig, self).ready()

