# encoding: utf-8

import stripe
import json

from workon import settings as workon_settings
from django.conf import settings
from django import forms
from django.db import models
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect


stripe.api_key = workon_settings.WORKON_STRIPE_SECRET_KEY

class StripeObject(models.Model):

    created_date = models.DateTimeField(u"Date création", auto_now_add=True)
    updated_date = models.DateTimeField(u"Date mise à jour", auto_now=True, db_index=True)

    id = models.CharField(u"ID Stripe", max_length=255, primary_key=True)
    data = models.TextField(u"Data Stripe", null=True, blank=True)

    class Meta:
        abstract = True

    def get_data(self, name=None):
        data = json.loads(self.data)
        if name:
            return data.get(name)
        else:
            return data

    def get_endpoint(self):
        return getattr(stripe, self.__class__.__name__.replace('Stripe', ''))

    def update(self):
        pass

    # def create(self, *args, **kwargs):
    #     endpoint = self.get_endpoint()
    #     endpoint.create(**kwargs)






class StripePlan(StripeObject):
    pass

class StripeTransfer(StripeObject):
    pass


class StripeCustomer(StripeObject):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True)
    user_email = models.CharField(max_length=254, null=True)

    def __str__(self):
        return str(self.user)

class StripeCard(StripeObject):
    pass


class StripeSubscription(StripeObject):

    customer = models.ForeignKey("workon.StripeCustomer", related_name="subscriptions")
    plan = models.ForeignKey("workon.StripePlan", null=True, related_name="subscriptions")

    @property
    def stripe_subscription(self):
        return stripe.Customer.retrieve(self.customer.stripe_id).subscriptions.retrieve(self.stripe_id)

class StripeInvoice(StripeObject):

    customer = models.ForeignKey("workon.StripeCustomer", related_name="invoices")
    charge = models.ForeignKey("workon.StripeCharge", null=True, related_name="invoices")
    subscription = models.ForeignKey("workon.StripeSubscription", null=True)

    @property
    def status(self):
        return "Paid" if self.paid else "Open"

class StripeInvoiceItem(models.Model):

    invoice = models.ForeignKey("workon.StripeInvoice", related_name="items")
    subscription = models.ForeignKey("workon.StripeSubscription", null=True)
    plan = models.ForeignKey("workon.StripePlan", null=True)

    def plan_display(self):
        return self.plan.name if self.plan else ""

class StripeCharge(StripeObject):

    customer = models.ForeignKey("workon.StripeCustomer", related_name="charges")
    invoice = models.ForeignKey("workon.StripeInvoice", null=True, related_name="charges")




class StripeEvent(StripeObject):
    is_executed = models.BooleanField(u"Executé ?", default=False)
    type = models.CharField(u"Type", max_length=254, db_index=True, null=True, blank=True)
    exec_errors = models.TextField(u"Import errors", null=True, blank=True)

    def save(self, *args, **kwargs):
        self.type = self.get_data('type')
        if not self.is_executed:
            try:
                self.execute()
                self.exec_errors = None
            except:
                self.exec_errors = traceback.format_exc()
                self.is_executed = False
        super(StripeEvent, self).save(*args, **kwargs)


    def execute(self):

        stripe_object = self.get_data('data')['object']

        if self.type == "charge.succeeded":
            payment, created = StripePayment.objects.get_or_create(id=stripe_object['id'])
            payment.data = data
            payment.save()
            self.is_executed = True

        elif self.type == "invoice.created":
            invoice, created = StripeInvoice.objects.get_or_create(id=stripe_object['id'])
            invoice.data = data
            invoice.save()
            self.is_executed = True

        elif self.type == "plan.deleted":
            subscription = StripeSubscription.objects.get_or_create(id=stripe_object['id'])
            subscription.delete()
            self.is_executed = True

        elif self.type == "invoice.payment_succeeded":
            invoice, created = StripeInvoice.objects.get_or_create(id=stripe_object['id'])
            invoice.data = data
            invoice.save()
            self.is_executed = True
