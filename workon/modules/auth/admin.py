# encoding: utf-8

from django.conf import settings
from django.contrib import admin
from django.db import models
from django import forms
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from .models import *

class ActivationTokenAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'is_used', 'activation_date', 'expiration_date', 'created_date', 'updated_date')
    search_fields = ('email', 'token', 'activation_date', 'created_date' )
    list_filter = ('is_used', )

    def get_readonly_fields(self, *args, **kwargs):
        fields = [f.name for f in self.model._meta.fields]
        return fields
admin.site.register(ActivationToken, ActivationTokenAdmin)

