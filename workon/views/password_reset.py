# encoding: utf-8

from django import forms
from django.conf import settings
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect, get_object_or_404
from django.utils.http import base36_to_int, int_to_base36
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator


class PasswordResetForm(forms.Form):

    email = forms.EmailField(label=_("Email"), required=True)

    def clean_email(self):
        User = get_user_model()
        value = self.cleaned_data["email"]
        if not User.objects.filter(email__iexact=value).exists():
            raise forms.ValidationError(_("Email address can not be found."))
        return value


class PasswordReset(generic.FormView):

    template_name = "user/password_reset.html"
    template_name_sent = "user/password_reset_sent.html"
    form_class = PasswordResetForm
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

