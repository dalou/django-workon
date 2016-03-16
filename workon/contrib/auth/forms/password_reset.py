# encoding: utf-8

from django import forms
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

import workon.utils



class PasswordResetToken(forms.Form):

    password = forms.CharField(
        label=_(u"Mot de passe"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_confirm = forms.CharField(
        label=_(u"Mot de passe (confirmation)"),
        widget=forms.PasswordInput(render_value=False)
    )

    def clean_password_confirm(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(_(u"Le mot de passe de confirmation doit correspondre."))
        return self.cleaned_data["password_confirm"]



class PasswordReset(forms.Form):

    email = forms.EmailField(label=_("Email"), required=True)

    def clean_email(self):
        User = get_user_model()
        value = self.cleaned_data["email"]
        if not User.objects.filter(email__iexact=value).exists():
            raise forms.ValidationError(_("Email address can not be found."))
        return value