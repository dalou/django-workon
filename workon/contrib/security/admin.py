# encoding: utf-8

from django.conf import settings
from django.contrib import admin

from .models import *


class DisallowedHostAdmin(admin.ModelAdmin):


    list_display = ('http_host', 'request_uri', 'path_info', 'remote_addr', 'http_x_forwarded_for', 'request_method', 'created_at')
    list_filter = ('http_host', 'request_uri', 'path_info', 'remote_addr', 'http_x_forwarded_for', 'request_method', )

    def get_readonly_fields(self, *args, **kwargs):
        fields = [f.name for f in self.model._meta.fields]
        return fields

admin.site.register(DisallowedHost, DisallowedHostAdmin)
