# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-19 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_discussion', '0002_post_date_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
