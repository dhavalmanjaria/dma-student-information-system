# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-23 11:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('examinations', '0006_auto_20170323_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examtimetable',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum.Subject'),
        ),
    ]