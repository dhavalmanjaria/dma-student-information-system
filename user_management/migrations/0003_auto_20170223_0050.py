# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 19:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_basicinfo_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinfo',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]
