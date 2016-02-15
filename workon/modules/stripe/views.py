# encoding: utf-8

import stripe

from django.contrib import auth, messages
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import *

stripe.api_key = workon_settings.WORKON_STRIPE_SECRET_KEY

@require_POST
@csrf_exempt
def webhook(request):
    event_json = json.loads(request.body)
    event = stripe.Event.retrieve(event_json["id"])
    event, created = StripeEvent.objects.get_or_create(id=event_json["id"])
    event.event_body = request.body
    event.save()
    return HttpResponse(status=200)
