# encoding: utf-8

import logging

from django.conf import settings
from django.db.models import get_model
from django.core.management.base import BaseCommand

from django.conf import settings
from django.contrib.sites.models import Site

class Command(BaseCommand):


    help = "Little help to describe the command" \
        "\n  usage:   ./manage.py set_site_domain [options]"


    def add_arguments(self, parser):
        parser.add_argument('domain')

    def handle(self, domain, *args, **options):

        site = Site.objects.get(id=settings.SITE_ID)
        site.domain = domain
        site.name = domain
        site.save()