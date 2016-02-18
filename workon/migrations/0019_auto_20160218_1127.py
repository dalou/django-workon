# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workon', '0018_auto_20160215_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selection',
            name='description',
            field=models.TextField(max_length=254, null=True, verbose_name='Description', blank=True),
        ),
    ]
