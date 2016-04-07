# encoding: utf-8
from django.conf import settings
from django.core.urlresolvers import NoReverseMatch
from django.views import generic
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from ..models import ActivationToken

import workon.utils

class Activate(generic.View):

    def get(self, request, token, *args, **kwargs):
        token = workon.utils.get_activation_token(token)
        if token:
            user = token.activate_user()
            if user:
                if workon.utils.authenticate_user(request, user, remember=True):
                    activation_message = getattr(settings, 'WORKON_AUTH_ACTIVATION_MESSAGE', u"Votre compte à bien été activé.")
                    if activation_message:
                        messages.success(request, activation_message)
                    activation_fallback_url = getattr(settings, 'WORKON_AUTH_ACTIVATION_FALLBACK_URL', None)
                    if not activation_fallback_url:
                        return "/"
                    try:
                        return HttpResponseRedirect(reverse(activation_fallback_url))
                    except NoReverseMatch:
                        return HttpResponseRedirect("/%s" % activation_fallback_url.lstrip('/'))

                    # elif activation_fallback_url.find(':') != -1:
                    #     return HttpResponseRedirect(reverse(activation_fallback_url))
                    # else:
                    #     return HttpResponseRedirect(activation_fallback_url)

        else:
            raise Http404