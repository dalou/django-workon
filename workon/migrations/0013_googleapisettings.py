# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workon', '0012_auto_20151215_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleAPISettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_key_file', models.FileField(upload_to=b'workon/googleapisettings/', null=True, verbose_name='Adresse email', blank=True)),
            ],
            options={
                'verbose_name': 'Param\xe8tres API Google',
                'verbose_name_plural': 'Param\xe8tres API Google',
            },
        ),
    ]
