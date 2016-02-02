# encoding: utf-8

import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from workon.utils import send_html_email
import subprocess

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Little help to describe the command" \
        "\n  usage:   ./manage.py notify_push"


    def handle(self, *args, **options):

        receivers = getattr(settings, 'WORKON_PUSH_NOTIFY_RECEIVERS', [])
        sender = getattr(settings, 'WORKON_PUSH_NOTIFY_SENDER', settings.DEFAULT_FROM_EMAIL)
        git = getattr(settings, 'WORKON_PUSH_NOTIFY_GIT', True)

        if receivers:

            html = u"""Mise à niveau du site effectuée avec succès ;)<br/><br/>"""

            if git:
                try:
                    head = subprocess.Popen("git log -1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    infos = head.stdout.read()
                    html += u"Informations : <br/><pre>%s</pre><br/>" % infos
                    html += u"<br/><br/>"
                except:
                    infos = u'unknown'

                print infos


            html += u"""<small>(Message automatique envoyé lors d'une mise à niveau du site en production)</small>"""


            send_html_email(
                subject=u"[Lechti.fr] Mise à niveau",
                sender=sender,
                receivers=receivers,
                html=html
            )