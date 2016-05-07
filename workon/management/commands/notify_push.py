# encoding: utf-8

import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from workon.utils import send_html_email
import subprocess

from ...utils import get_project_title

logger = logging.getLogger(__name__)

"""
Example of use on distant push with git comment logging :
heroku run python manage.py notify_push --comment "$(shell git log -1)" --remote production
"""

class Command(BaseCommand):
    help = "Little help to describe the command" \
        "\n  usage:   ./manage.py notify_push"

    def add_arguments(self, parser):
        parser.add_argument('--comment', nargs='+', type=unicode)

    def handle(self, *args, **options):


        receivers = getattr(settings, 'WORKON_PUSH_NOTIFY_RECEIVERS', [])
        sender = getattr(settings, 'WORKON_PUSH_NOTIFY_SENDER', settings.DEFAULT_FROM_EMAIL)
        subject = getattr(settings, 'WORKON_PUSH_NOTIFY_SUBJECT', u"[%s] Mise à niveau" % get_project_title())

        if receivers:

            html = u"""Mise à niveau du site effectuée avec succès<br/><br/>"""


            if options.get('comment'):
                html += u"Informations : <br/><pre>%s</pre><br/><br/>" % ",".join(options.get('comment')).replace('   ', '<br/>')


            html += u"""<small>(Ceci est un message automatique envoyé lors d'une mise à niveau du site en production</small>"""


            send_html_email(
                subject=subject,
                sender=sender,
                receivers=receivers,
                html=html
            )