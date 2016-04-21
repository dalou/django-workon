# encoding: utf-8

from django import forms
from django.conf import settings
from django.views import generic
from django.contrib import auth
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect

import workon.forms
import workon.utils
import workon.signals

class Login(generic.FormView):
    template_name = "auth/login.html"
    template_name_ajax = "auth/_login.html"
    form_class = workon.forms.Login
    form_kwargs = {}
    redirect_field_name = "next"

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(self.get_success_url())
        return super(Login, self).get(*args, **kwargs)

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.template_name_ajax]
        else:
            return [self.template_name]

    def get_context_data(self, *args, **kwargs):
        ctx = super(Login, self).get_context_data(*args, **kwargs)
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.POST.get(redirect_field_name, self.request.GET.get(redirect_field_name, "")),
        })
        return ctx

    def get_form_kwargs(self):
        kwargs = super(Login, self).get_form_kwargs()
        kwargs.update(self.form_kwargs)
        return kwargs

    def form_invalid(self, form):

        if form.prefix:
            key = "-".join([form.prefix, "email"])
        else:
            key = "email"
        username = form.data.get(key, None)

        workon.signals.user_login_attempt.send(
            sender=Login,
            username=username,
            result=form.is_valid()
        )
        return super(Login, self).form_invalid(form)


    def after_form_valid(self, form):
        workon.utils.authenticate_user(self.request, form.user, remember=form.cleaned_data.get("remember"))

    def form_valid(self, form):
        self.after_form_valid(form)
        return redirect(self.get_success_url())


    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = '/%s' % (settings.PREFIX_URL if hasattr(settings, 'PREFIX_URL') else "")
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return workon.utils.default_redirect(self.request, fallback_url, **kwargs)

    def get_redirect_field_name(self):
        return self.redirect_field_name