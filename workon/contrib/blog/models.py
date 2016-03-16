# encoding: utf-8

import datetime

from django.db import models
from django.conf import settings
from django.utils.text import slugify

import workon.models
import workon.fields
import workon.utils

class Publishable(models.Model):

    class Meta:
        abstract = True

    created_date = models.DateTimeField(u"Date created", auto_now_add=True)
    updated_date = models.DateTimeField(u"Date updated", auto_now=True, db_index=True)

    meta_title = models.CharField(u"Meta titre", max_length=254, blank=True, null=True)
    meta_description = models.TextField(u"Meta description", max_length=254, blank=True, null=True)

    published_date = models.DateTimeField(verbose_name=u"Date de publication", blank=True, null=True)
    is_published = models.BooleanField(u"Publiée ?", default=False)
    is_publishable = models.BooleanField(u"Publiable ?", default=False)
    is_active = models.BooleanField(u"Activée ?", default=True)
    is_fake = models.BooleanField(u"Fake ?", default=False)
    is_draft = models.BooleanField(u"Brouillon ?", default=True)
    imported_from = models.CharField(u"Importé de", max_length=254, blank=True, null=True)

    random_position = models.PositiveIntegerField(u"Position aleatoire journalière", blank=True, null=True)

    STATUS_NEW, STATUS_REJECTED, STATUS_VALIDATED, STATUS_EXPIRED, STATUS_DISABLED = ('NEW', 'REJECTED', 'VALIDATED', 'EXPIRED', 'DISABLED')
    STATUS_CHOICES = (
        (STATUS_NEW, u"Nouveau"),
        (STATUS_REJECTED, u"Rejetée"),
        (STATUS_VALIDATED, u"Validée"),
        (STATUS_EXPIRED, u"Expirée"),
        (STATUS_DISABLED, u"Désactivée")
    )
    status = models.CharField(max_length=254, choices=STATUS_CHOICES, default=STATUS_NEW, verbose_name=u"Status", null=False, blank=False)

    geo_address = models.CharField(u'Adresse géolocalisée', max_length=254, blank=True, null=True)
    geo_latitude = models.FloatField(u'lat', blank=True, null=True)
    geo_longitude = models.FloatField(u'lon', blank=True, null=True)
    geo_formatted_address = models.CharField(u'Adresse géocodée & formattée', max_length=254, blank=True, null=True)
    geo_gmaps_results = workon.fields.JSONField(u'Geodata', default={}, blank=True, null=True)

    def publishable(self):
        return True