# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-05-20 18:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examinations', '0007_auto_20170323_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='academic_year',
            field=models.PositiveIntegerField(default=2018, help_text='Year that the academic year started in.'),
        ),
    ]
