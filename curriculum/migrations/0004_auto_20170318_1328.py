# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-18 07:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0003_subject_is_university_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='is_university_subject',
            field=models.BooleanField(default=True),
        ),
    ]
