# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workon', '0011_auto_20151215_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailing',
            name='send_range',
            field=models.IntegerField(default=100, help_text="Les tranches d'envois permette de soulager le serveur d'envoi de masse.", verbose_name="Tranche d'envois maximum par session", choices=[(20, 20), (50, 50), (70, 70), (100, 100), (200, 200), (500, 500), (1000, 1000)]),
        ),
    ]
