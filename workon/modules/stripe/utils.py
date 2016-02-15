import stripe

from workon import settings as workon_settings
from django.conf import settings
from .models import *

stripe.api_key = workon_settings.WORKON_STRIPE_SECRET_KEY


def stripe_charge_plan(token, plan_id, description=None, email=None, metadata={}):

    plan = StripePlan.objects.get(id=plan_id)

    customer = stripe.Customer.create(
        description=description if description else "Customer for %s (%s)" % (plan.id, email),
        source=token, # obtained with .js
        email=email,
        metadata=metadata,
        plan=plan.id
    )

def stripe_create_plan(id, name, amount, currency="eur", interval="month", metadata={}):

    plan = StripePlan.objects.get_or_create(id=id)
    data = stripe.Plan.create(
        id=id,
        name=name,
        amount=amount,
        interval=interval,
        currency=currency,
        metadata=metadata
    )
    plan.data = data
    plan.save()