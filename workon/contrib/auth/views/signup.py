# encoding: utf-8
from django import forms
from django.conf import settings
from django.views import generic
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone

import workon.utils
import workon.forms


class Signup(generic.FormView):

    template_name = "auth/signup.html"
    #template_name_ajax = "auth/_signup.html"
    form_class = workon.forms.Signup

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(reverse('user:dashboard'))
        # if not self.is_open():
        #     return self.closed()
        return super(Signup, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            raise Http404()
        # if not self.is_open():
        #     return self.closed()
        return super(Signup, self).post(*args, **kwargs)

    def get_initial(self):
        initial = super(Signup, self).get_initial()
        # if self.is_invitation:
        #     initial["invitation_hash"] = self.get_invitation_hash()
        if self.request.GET.get('email'):
            initial["email"] = self.request.GET.get('email')
        return initial


    def form_valid(self, form):

        user = workon.utils.get_or_create_user(
            form.cleaned_data["email"],
            username = form.cleaned_data["username"],
            first_name = form.cleaned_data["first_name"],
            last_name = form.cleaned_data["last_name"],
            is_active = False,
            expiration_date = timezone.now(),
            password = form.cleaned_data.get("password"),
            phone_number = form.cleaned_data.get("phone_number"),
            save = True
        )
        self.after_form_valid(form, user)
        return self.success_return(form, user)

    def after_form_valid(self, form, user):
        return

    def success_return(self, form, user):
        return redirect(self.get_success_url())


    def form_invalid(self, form):
        return super(Signup, self).form_invalid(form)

    def get_success_url(self, fallback_url=None, **kwargs):
        return '/'
