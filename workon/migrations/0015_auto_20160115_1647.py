# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workon', '0014_auto_20160113_1714'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailinguseractivationtoken',
            options={'ordering': ('created_date', 'activation_date'), 'verbose_name': "Cl\xe9 d'activation", 'verbose_name_plural': "Cl\xe9s d'activation"},
        ),
    ]
