# encoding: utf-8

from django.conf import settings
from django import forms
from django.db.models import Q, Count
from django.views import generic
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.shortcuts import render


class Save(generic.UpdateView):

    def get_object(self, *args, **kwargs):
        if hasattr(self, '_object'):
            return getattr(self, '_object')
        self.created = False
        try:
            self.object = super(Save, self).get_object()
        except AttributeError:
            self.object = self.model()
            self.created = True

        setattr(self, '_object', self.object)
        return self.object

class FlexibleUpdate(generic.UpdateView):

    template_name = "workon/views/_flexible_update.html"
    # template_success_name = "organization/view/_view.html"
    fields = [

    ]
    creation = False
    default_fields = []


    def get_queryset(self, *args, **kwargs):
        return super(FlexibleUpdate, self).get_queryset(*args, **kwargs)

    def has_permission(self, request, object):
        return True

    def is_request_allowed(self, request):
        return request.user.is_authenticated()

    # def form_invalid(self, form, **forms):
    #     return JsonResponse({ 'errors' : form.errors }, status=200)

    def get_object(self, *args, **kwargs):
        if hasattr(self, '_object'):
            return getattr(self, '_object')

        self.created = False

        if not self.is_request_allowed(self.request):
            raise Http404
        else:
            if not self.creation:
                self.object = super(FlexibleUpdate, self).get_object()
            else:
                try:
                    self.object = super(FlexibleUpdate, self).get_object()
                except AttributeError, e:
                    print str(e.message)
                    self.object = self.model()
                    self.created = True

        if not self.has_permission(self.request, self.object):
            raise Http404

        if self.request.method == "POST" :
            fields = self.request.POST.keys()
            fields += self.request.FILES.keys()
        else:
            fields = self.request.GET.getlist('field[]', self.default_fields)

        current_fields = []
        for name in fields:
            if name in self.fields and hasattr(self.object, name) or hasattr(self.model, name):
                current_fields.append(name)
        self.fields = current_fields
        setattr(self, '_object', self.object)
        return self.object

    def get_form_valid_json(self, form):
        return {}


    def get_form(self, *args, **kwargs):
        form = super(FlexibleUpdate, self).get_form(*args, **kwargs)
        return form

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save()
        # self.object.set_initials()

        if self.request.is_ajax():
            json = self.get_form_valid_json(form)
            return JsonResponse(json, status=200, safe=False)
        else:
            return HttpResponseRedirect(self.object.get_absolute_url() + '?edit=1')

    def get_context_data(self, **kwargs):
        ctx = super(FlexibleUpdate, self).get_context_data(**kwargs)
        ctx['title'] = self.request.GET.get('title')
        ctx['display_labels'] = self.request.GET.get('display_labels') == "1"
        return ctx