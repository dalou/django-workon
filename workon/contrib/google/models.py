# encoding: utf-8

from django.conf import settings
from django.db import models
from django.utils import timezone

from ...models import Unique

class GoogleAPISettings(Unique):

    account_key_file = models.FileField(u"Adresse email", upload_to="workon/googleapisettings/", null=True , blank=True, help_text=u"""

            Allez sur <a target="_blank" href="https://console.developers.google.com/apis/">https://console.developers.google.com/apis/</a>
            <br/>
            Cliquer sur identifiants
            <br/>
            Cliquer sur nouveaux identifiants
            <br/>
            Cliquer sur Créér un compte de service
            <br/>
            Nommer le compte, copier/coller l'ID du compte de service, puis cocher JSON
            <br/>
            Cliquer sur Créér
            <br/>
            Ajouter le compte (ID copier/coller) en lecture seule dans votre compte analytics (<a target="_blank" href="https://www.google.com/analytics/web/">https://www.google.com/analytics/web/</a>)
            <br/>
            Puis ajouter ici le fichier telechargé depuis la page Google Developpers Console (aprés avoir cliqué sur Créér)

        """)
    analytics_default_view_id = models.CharField(u"ID de la vue Analytics par defaut.", max_length=254, null=True , blank=True)


    class Meta:
        verbose_name = u"Paramètres API Google"
        verbose_name_plural = u"Paramètres API Google"
