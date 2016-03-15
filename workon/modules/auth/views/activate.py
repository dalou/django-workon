# encoding: utf-8
from django.conf import settings
from django.views import generic
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

import workon.utils

class Activate(generic.View):

    def get(self, request, token, *args, **kwargs):
        try:
            token = workon.utils.get_activation_token(token)
            if token:
                user = token.activate_user()
                if user:
                    if workon.utils.authenticate_user(request, user, remember=True):
                        messages.success(request, u"Votre compte à bien été activé.")
                        return HttpResponseRedirect(reverse('user:dashboard'))

        except EmailingUserActivationToken.DoesNotExist:
            pass
        raise Http404