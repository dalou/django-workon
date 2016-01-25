# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workon', '0010_auto_20151215_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailingtransaction',
            name='emailing',
            field=models.ForeignKey(related_name='transactions', to='workon.Emailing'),
        ),
    ]
