# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 12:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internal_assessment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='metric',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='studentmetric',
            options={'ordering': ('metric',)},
        ),
    ]
