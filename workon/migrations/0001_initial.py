# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import workon.fields.html


class Migration(migrations.Migration):


    operations = [
        migrations.CreateModel(
            name='Emailing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Cr\xe9\xe9 le')),
                ('name', models.CharField(max_length=254, verbose_name='Nom')),
                ('subject', models.CharField(max_length=254, null=True, verbose_name='Sujet du mail', blank=True)),
                ('receivers', models.TextField(null=True, verbose_name='Adresses emails', blank=True)),
                ('template', models.TextField(verbose_name='Template du mail')),
                ('template_name', models.TextField(null=True, verbose_name='Template name', blank=True)),
                ('is_sent', models.BooleanField(default=False, verbose_name='Envoy\xe9 ?')),
            ],
            options={
                'ordering': ('-date_created',),
                'verbose_name': 'Email group\xe9',
                'verbose_name_plural': 'Emails group\xe9s',
            },
        ),
        migrations.CreateModel(
            name='EmailingTestEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Adresse email')),
            ],
        ),
        migrations.CreateModel(
            name='EmailingTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Cr\xe9\xe9 le')),
                ('receiver', models.EmailField(max_length=254, verbose_name='Adresse email')),
                ('is_sent', models.BooleanField(default=False, verbose_name='Envoy\xe9 ?')),
                ('email', models.ForeignKey(to='workon.Emailing')),
            ],
            options={
                'ordering': ('-date_created',),
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.CreateModel(
            name='EmailingUserActivationToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='Adresse email', db_index=True)),
                ('token', models.CharField(unique=True, max_length=64, verbose_name="Token d'activation", db_index=True)),
                ('is_used', models.BooleanField(default=False, verbose_name='Utilis\xe9 ?')),
                ('expiration_date', models.DateTimeField(null=True, verbose_name="date d'expiration", blank=True)),
            ],
        ),
    ]
