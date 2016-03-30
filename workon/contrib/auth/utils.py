from __future__ import unicode_literals

import functools
try:
    from urllib.parse import urlparse, urlunparse
except ImportError:  # python 2
    from urlparse import urlparse, urlunparse
from django.conf import settings
from django.core import urlresolvers
from django.contrib import auth
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseRedirect, QueryDict
from django.contrib.auth import get_user_model
from django.utils import timezone

import workon.utils


def get_activation_token(token, is_used=False):
    from .models import ActivationToken
    try:
        return ActivationToken.objects.get(token=token, is_used=is_used)
    except:
        return None

def get_valid_activation_token(email, is_used=False):
    from .models import ActivationToken
    email = workon.utils.is_valid_email(email)
    if email:
        return ActivationToken.objects.filter(
            email=email,
            is_used=is_used,
            expiration_date__gt=timezone.now()
        ).first()
    return None

def create_activation_token(email, expiration_date=None):
    from .models import ActivationToken
    email = workon.utils.is_valid_email(email)
    if email:
        activation_token, created = ActivationToken.objects.get_or_create(
            email=email,
            is_used=False,
        )
        activation_token.expiration_date = expiration_date
        activation_token.save()
        return activation_token
    return None

def authenticate_user(request, user, remember=True, backend=None, expiry=60 * 60 * 24 * 365 * 10):
    if not hasattr(user, 'backend'):
        if backend:
            user.backend = backend
        elif hasattr(settings, 'AUTHENTICATION_BACKENDS') and len(settings.AUTHENTICATION_BACKENDS):
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
        else:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
    if request.user.is_authenticated():
        auth.logout(request)
    auth.login(request, user)
    request.session.set_expiry(expiry if remember else 0)
    return True



def get_or_create_user(email, username=None, first_name=None, last_name=None,
                        is_active=False, expiration_date=None, set_names_from_email=False,
                        password=None, save=True):
    User = get_user_model()
    email = workon.utils.is_valid_email(email)
    if email:
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            user = User(
                email = email.strip(),
                username = username.strip() if username else None,
                first_name = first_name.strip() if first_name else None,
                last_name = last_name.strip() if last_name else None,
                is_active = is_active,
                # expiration_date = expiration_date
            )
            if password:
                user.set_password(password)
            else:
                user.set_unusable_password()
            if set_names_from_email:

                if not user.username:
                    user.username = email.split('@')[0][0:254]

                if not user.first_name and not user.last_name:
                    user_names = user.username.split('.', 2)
                    if len(user_names) == 2:
                        user.first_name = ''.join([i for i in user_names[0].capitalize() if not i.isdigit()])
                        user.last_name = ''.join([i for i in user_names[1].capitalize() if not i.isdigit()])
                    else:
                        user.first_name = ''.join([i for i in user_names[0].capitalize() if not i.isdigit()])
            if save:
                user.save()
        return user
    else:
        return None
