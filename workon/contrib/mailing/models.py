# encoding: utf-8
import datetime
import operator
import hashlib
import urllib
import random
import re

from django.conf import settings
from django.db import models
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse

import workon.utils



class Emailing(models.Model):
    created_at = models.DateTimeField(u"Créé le", auto_now_add=True)
    updated_at = models.DateTimeField(u"Modifié le", auto_now=True, db_index=True)

    subject = models.CharField(u"Objet du mail", max_length=254, blank=True, null=True)
    sender = models.CharField(u"De", max_length=254, blank=True, null=True)

    receivers = models.TextField(u"Vers (destinations réélles)", blank=True, null=True)
    receivers_test = models.TextField(u"Vers (destination de test)", blank=True, null=True)
    template = models.TextField(u"Template", help_text=u"""
        Pour inserer un lien d'activation de compte utilisez : <b>*|ACTIVATE_URL|*</b>.<br />
        exemple : <b>&lt;a href="*|ACTIVATE_URL|*"&gt;Cliquez ici pour votre connecter&lt;/a&gt;</b>
    """)
    # template_name = models.TextField(u"Template name", blank=True, null=True)
    send_count = models.IntegerField(u"Compteur d'envois", default=0)
    test_count = models.IntegerField(u"Compteur de tests", default=0)

    class Meta:
        verbose_name = u"Email groupé"
        verbose_name_plural = u"Emails groupés"
        ordering = ('-created_date',)


    def get_transaction_send_count(self):
        return self.transactions.exclude(send_count=0).count()

    def get_send_count_remind(self):
        receivers = self.receivers.split(',')
        return  max(0, len(receivers) - self.get_transaction_send_count())

    def __repr__(self):
        sent = ""
        if self.send_count > 0:
            sent = u" (Envoyé)"
        return u"{0} - {1}{2}".format(self.name, self.subject, sent)


    def send(self, force=False, test=True):
        final_receivers = []
        if self.pk:
            activate_url = re.search(r'\*\|ACTIVATE_URL\|\*', self.template)
            archive_url = re.search(r'\*\|ARCHIVE\|\*', self.template)
            mc_subject = re.search(r'\*\|MC:SUBJECT\|\*', self.template)

            receivers = self.receivers_test if test else self.receivers
            receivers = receivers.split(',')
            messages = []

            irange = 0

            for receiver in receivers:
                receiver = receiver.strip()
                if workon.utils.is_valid_email(receiver):


                    html = self.template
                    html = workon.utils.set_mailchimp_vars(html)

                    if activate_url:
                        activation_token = workon.utils.create_activation_token(receiver)
                        html = html.replace(
                            activate_url.group(0),
                            workon.utils.build_absolute_url(activation_token.get_absolute_url())
                        )

                    # if archive_url:
                    #     html = html.replace(archive_url.group(0), self. )

                    if mc_subject:
                        html = html.replace(mc_subject.group(0), self.subject )

                    html = workon.utils.clean_html_for_email(html)

                    if not test:
                        transaction, created = EmailingTransaction.objects.get_or_create(
                            receiver=receiver,
                            emailing=self
                        )
                    else:
                        created = True
                    if irange < self.send_range and (created or transaction.send_count == 0):
                        message = workon.utils.HtmlTemplateEmail(
                            subject=self.subject,
                            sender=self.sender,
                            receivers=[receiver],
                            html=html,
                        )
                        messages.append(message)
                        final_receivers.append(receiver)
                        if not test:
                            transaction.send_count += 1
                            transaction.save()
                        irange += 1

            workon.utils.send_mass_email(messages)
            if test:
                self.test_count += 1
            else:
                self.send_count += 1
            self.save()
        return final_receivers



class EmailingTransaction(models.Model):

    created_date = models.DateTimeField(u"Créé le", auto_now_add=True)
    updated_date = models.DateTimeField(u"Modifié le", auto_now=True, db_index=True)

    emailing = models.ForeignKey('workon.Emailing', related_name="transactions")
    receiver = models.EmailField(u"Adresse email", max_length=254)
    send_count = models.IntegerField(u"Compteur d'envois", default=0)

    class Meta:
        verbose_name = u"Email - Transaction"
        verbose_name_plural = u"Email - Transactions"
        ordering = ('-created_date',)

    def __unicode__(self):
        sent = ""
        if self.send_count > 0:
            sent = u" (Envoyé)"
        return u"{0}{1}".format(self.emailing.name, sent)



class EmailingTestEmail(models.Model):
    email = models.EmailField(u"Adresse email", max_length=254)






