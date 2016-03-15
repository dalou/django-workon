# encoding: utf-8

import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response

import workon.utils
import workon.models
import workon.fields


def test_send_html_mail(request):
    if request.GET.get('send') == '1':
        workon.utils.send_template_email(
            u"Test Envoi HTML",
            u"Workon test station <no-reply@workon.io>",
            ['autrusseau.damien@gmail.com'],
            template="user/email/activate.html",
            context={
                'absolute_uri': workon.utils.build_absolute_url(),
                'activate_url': workon.utils.build_absolute_url(self.get_absolute_activate_url())
            }
        )
        return redirect(reverse('test_send_html_mail'))
    else:
        return render_to_response('test_send_html_mail', {

        })