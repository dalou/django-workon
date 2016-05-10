import stripe

from workon import settings as workon_settings
from django.conf import settings

stripe.api_key = workon_settings.WORKON_STRIPE_SECRET_KEY

def stripe_charge(token, amount, currency="eur", description=None, metadata={}):
    from .models import StripeCharge

    charge = StripeCharge.get_or_create(
        amount=amount,
        currency=currency,
        description=description if description else "Charge %s" % (amount,),
        source=token, # obtained with .js
        metadata=metadata,
    )
    return charge

def stripe_charge_plan(token, plan_id, description=None, email=None, metadata={}):
    from .models import StripePlan, StripeCustomer

    plan = StripePlan.objects.get(id=plan_id)

    customer = StripeCustomer.get_or_create(
        description=description if description else "Customer for %s (%s)" % (plan.id, email),
        source=token, # obtained with .js
        email=email,
        metadata=metadata,
        plan=plan.id
    )
    return customer

def stripe_create_plan(id, name, amount, currency="eur", interval="month", metadata={}):
    from .models import StripePlan
    plan = StripePlan.get_or_create(
        id=id,
        name=name,
        amount=amount,
        interval=interval,
        currency=currency,
        metadata=metadata
    )
    return plan