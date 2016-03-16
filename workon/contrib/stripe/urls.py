# encoding: utf-8
from workon import settings
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    url(r'^%s$' % (settings.WORKON_STRIPE_WEBHOOK_URL), views.webhook, name="stripe-webhook"),
]