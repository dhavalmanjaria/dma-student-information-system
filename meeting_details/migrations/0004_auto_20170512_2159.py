# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-12 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting_details', '0003_auto_20170512_2118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='date_and_time',
        ),
        migrations.AddField(
            model_name='meeting',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]
