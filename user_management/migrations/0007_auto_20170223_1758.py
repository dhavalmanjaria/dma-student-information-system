# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0006_auto_20170223_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authenticationrequest',
            name='request_date',
            field=models.DateField(auto_now=True),
        ),
    ]