# encoding: utf-8

import datetime
import operator

from django.contrib import admin
from django.db import models

from .models import *

from ..unique.admin import UniqueAdmin

class GoogleAPISettingsAdmin(UniqueAdmin):
    pass
admin.site.register(GoogleAPISettings, GoogleAPISettingsAdmin)