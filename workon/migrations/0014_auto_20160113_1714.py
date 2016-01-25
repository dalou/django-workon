# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workon', '0013_googleapisettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='googleapisettings',
            name='analytics_default_view_id',
            field=models.CharField(max_length=254, null=True, verbose_name='ID de la vue Analytics par defaut.', blank=True),
        ),
        migrations.AlterField(
            model_name='googleapisettings',
            name='account_key_file',
            field=models.FileField(help_text='\n            <div style="font-size:16px;">\n            Allez sur <a target="_blank" href="https://console.developers.google.com/apis/">https://console.developers.google.com/apis/</a>\n            <br/>\n            Cliquer sur identifiants\n            <br/>\n            Cliquer sur nouveaux identifiants\n            <br/>\n            Cliquer sur Cr\xe9\xe9r un compte de service\n            <br/>\n            Nommer le compte, copier/coller l\'ID du compte de service, puis cocher JSON\n            <br/>\n            Cliquer sur Cr\xe9\xe9r\n            <br/>\n            Ajouter le compte (ID copier/coller) en lecture seule dans votre compte analytics (<a target="_blank" href="https://www.google.com/analytics/web/">https://www.google.com/analytics/web/</a>)\n            <br/>\n            Puis ajouter ici le fichier telecharg\xe9 depuis la page Google Developpers Console (apr\xe9s avoir cliqu\xe9 sur Cr\xe9\xe9r)\n            </div>\n        ', upload_to=b'workon/googleapisettings/', null=True, verbose_name='Adresse email', blank=True),
        ),
    ]
