# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-10 08:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workon', '0021_auto_20160317_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stripecharge',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='charges', to='workon.StripeCustomer'),
        ),
    ]
