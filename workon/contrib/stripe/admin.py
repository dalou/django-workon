# encoding: utf-8

import stripe

from workon import settings as workon_settings
from django.conf import settings
from django import forms
from django.contrib import admin
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from .models import *
import django_select2.forms

stripe.api_key = workon_settings.WORKON_STRIPE_SECRET_KEY

print StripeEvent._meta.get_fields()

class StripeEventAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'type', 'is_executed', 'created_date')
    list_filter = ('type', )

    change_list_template = "workon/stripe/admin/event_list.html"


    readonly_fields = [f.name for f in StripeEvent._meta.get_fields()]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        js = [
            'client/event/admin.js'
        ]

admin.site.register(StripeEvent, StripeEventAdmin)


class StripePlanAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id')

    # readonly_fields = StripePlan._meta.get_all_field_names()

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        js = [
            'client/event/admin.js'
        ]

admin.site.register(StripePlan, StripePlanAdmin)
