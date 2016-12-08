# encoding: utf-8
from django import forms
from django.conf import settings
from django.views import generic
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from django.contrib import auth, messages
from django.contrib.auth import get_user_model

# from django_flow.utils import send_staff_notification, send_template_email


class Signup(forms.Form):

    first_name = forms.CharField(
        label=u"Prénom",
        required=False
    )

    last_name = forms.CharField(
        label=u"Nom",
        required=False
    )

    email = forms.EmailField(
        label=u"* Adresse e-mail",
        widget=forms.TextInput(),
        required=True,
    )

    username = forms.CharField(
        label=u"* Nom d'utilisateur / Pseudo",
        required=True
    )

    password = forms.CharField(
        label=u"* Mot de passe",
        widget=forms.PasswordInput(render_value=True)
    )

    password_confirm = forms.CharField(
        label=u"* Confirmer le mot de passe",
        widget=forms.PasswordInput(render_value=False)
    )

    accept_terms = forms.BooleanField(
        label=u"""J'accepte les <a data-modal="/conditions-dutilisation/" href="/conditions-dutilisation/">conditions d'utilisation</a>""" ,
        required=False
    )

    def clean_email(self):
        User = get_user_model()
        value = self.cleaned_data["email"]
        if not User.objects.filter(email__iexact=value).exists():
            return value
        raise forms.ValidationError(u"Un utilisateur est déjà enregistré avec cet adresse e-mail.")

    def clean_accept_terms(self):
        value = self.cleaned_data.get("accept_terms")
        # if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
        if not value:
            raise forms.ValidationError(u"Vous devez accepter les conditions d'utilisations.")
        return value

    def clean_password_confirm(self):
        value = self.cleaned_data["password_confirm"].strip()
        # if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
        if self.cleaned_data["password"].strip() != value:
            raise forms.ValidationError(u"Le mot de passe doit être le même.")
        return value

    def __init__(self, *args, **kwargs):
        super(Signup, self).__init__(*args, **kwargs)
        # del self.fields["username"]
        self.fields.keyOrder = ['email', 'password', 'password_confirm']

