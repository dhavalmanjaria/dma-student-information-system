# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 05:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0011_auto_20170214_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinfo',
            name='serial_no',
            field=models.CharField(help_text='Simpler unique identifier for this user', max_length=6, unique=True),
        ),
    ]
