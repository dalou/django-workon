# encoding: utf-8
import re
import datetime
import random

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class SocialMixin(models.Model):
    created_date = models.DateTimeField(u"Date created", auto_now_add=True)
    updated_date = models.DateTimeField(u"Date updated", auto_now=True, db_index=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content_type = models.ForeignKey(ContentType)
    instance_id = models.PositiveIntegerField()
    instance = generic.GenericForeignKey('content_type', 'instance_id')

    class Meta:
        abstract = True


class Favorite(SocialMixin):

    class Meta:
        abstract = True
        ordering = ["-created_date"]
        unique_together = ("user", "content_type", "instance_id")
        verbose_name = "Favori"
        verbose_name_plural = "Favoris"

    def __unicode__(self):
        return u"{} favorited {}".format(self.user, self.instance)




class AbuseReport(SocialMixin):

    message = models.TextField(u"Message", null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ["-created_date"]
        unique_together = ("user", "content_type", "instance_id")
        verbose_name = "Signalement"
        verbose_name_plural = "Signalements"

    def __unicode__(self):
        return u"{} reported {}".format(self.user, self.instance)




class Comment(SocialMixin):

    message = models.TextField(u"Message", null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ["-created_date"]
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"

    def __unicode__(self):
        return u"{} commented {}".format(self.user, self.instance)