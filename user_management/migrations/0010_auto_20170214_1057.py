# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 05:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0009_auto_20170214_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinfo',
            name='serial_no',
            field=models.CharField(default='298597', help_text='Simpler unique identifier for this user', max_length=6, unique=True),
        ),
    ]
