# encoding: utf-8

from django import forms
from django.conf import settings
from django.contrib import auth
from django.utils.translation import ugettext_lazy as _


class Login(forms.Form):

    email = forms.EmailField(label="Adresse e-mail")
    authentication_fail_message = _(u"L'adresse email ou le mot de passe que vous avez renseigné est incorrect.")

    password = forms.CharField(
        label=u"Mot de passe",
        widget=forms.PasswordInput(render_value=True)
    )
    remember = forms.BooleanField(
        label=u"Se souvenir de moi",
        required=False
    )
    user = None

    def clean(self):
        if self._errors:
            return
        user = auth.authenticate(
            username=self.cleaned_data["email"],
            password=self.cleaned_data["password"]
        )
        if user:
            if user.is_active:
                self.user = user
            else:
                self.add_error('email', "This account is inactive.")
        else:
            self.add_error('email', self.authentication_fail_message)
        return self.cleaned_data
