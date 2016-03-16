# encoding: utf-8

from django import forms
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect, get_object_or_404
from django.utils.http import base36_to_int, int_to_base36
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

import workon.utils
import workon.forms

class PasswordResetToken(generic.FormView):

    template_name = "auth/password_reset_token.html"
    template_name_fail = "auth/password_reset_token_fail.html"
    form_class = workon.forms.PasswordResetToken
    token_generator = default_token_generator
    redirect_field_name = "next"
    messages = {
        "password_changed": {
            "level": messages.SUCCESS,
            "text": _(u"Mot de passe changé avec succés.")
        },
    }

    def get(self, request, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ctx = self.get_context_data(form=form)
        if not self.check_token(self.get_user(), self.kwargs["token"]):
            return self.token_fail()
        return self.render_to_response(ctx)

    def get_context_data(self, **kwargs):
        ctx = kwargs
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "uidb36": self.kwargs["uidb36"],
            "token": self.kwargs["token"],
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.POST.get(redirect_field_name, self.request.GET.get(redirect_field_name, "")),
        })
        return ctx

    def change_password(self, form):
        user = self.get_user()
        user.set_password(form.cleaned_data["password"])
        user.save()

    def after_form_valid(self):
        user = self.get_user()
        if self.messages.get("password_changed"):
            messages.add_message(
                self.request,
                self.messages["password_changed"]["level"],
                self.messages["password_changed"]["text"]
            )

    def form_valid(self, form):
        self.change_password(form)
        self.after_form_valid()
        return redirect(self.get_success_url())

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = 'user:dashboard'
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return workon.utils.default_redirect(self.request, fallback_url, **kwargs)

    def get_user(self):
        try:
            uid_int = base36_to_int(self.kwargs["uidb36"])
        except ValueError:
            raise Http404()
        return get_object_or_404(get_user_model(), id=uid_int)

    def check_token(self, user, token):
        return self.token_generator.check_token(user, token)

    def token_fail(self):
        response_kwargs = {
            "request": self.request,
            "template": self.template_name_fail,
            "context": self.get_context_data()
        }
        return self.response_class(**response_kwargs)

    def send_email(self, user):
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        current_site = get_current_site(self.request)
        ctx = {
            "user": user,
            "protocol": protocol,
            "current_site": current_site,
        }
        hookset.send_password_change_email([user.email], ctx)




class PasswordReset(generic.FormView):

    template_name = "auth/password_reset.html"
    template_name_sent = "auth/password_reset_sent.html"
    form_class = workon.forms.PasswordReset
    token_generator = default_token_generator

    def get_context_data(self, *args, **kwargs):
        context = super(PasswordReset, self).get_context_data(*args, **kwargs)
        context.update(kwargs)
        if self.request.method == "POST" and "resend" in self.request.POST:
            context["resend"] = True
        return context

    def form_valid(self, form):
        User = get_user_model()
        try:
            user = User.objects.get(email__iexact=form.cleaned_data["email"])

            uid = int_to_base36(user.id)
            token = self.make_token(user)
            self.send_email(user, uid, token)

        except User.DoesNotExist:
            return self.form_invalid(form)

        response_kwargs = {
            "request": self.request,
            "template": self.template_name_sent,
            "context": self.get_context_data(form=form)
        }
        return self.response_class(**response_kwargs)

    def send_email(self, email, uid, token):
        raise NotImplementedError(u"Not implemented send_mail")


    def make_token(self, user):
        return self.token_generator.make_token(user)

