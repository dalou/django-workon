# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workon', '0020_auto_20160314_0805'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ActivationToken',
        ),
    ]
