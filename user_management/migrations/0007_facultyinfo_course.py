# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 22:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0002_subject_faculty'),
        ('user_management', '0006_auto_20170307_0321'),
    ]

    operations = [
        migrations.AddField(
            model_name='facultyinfo',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='curriculum.Course'),
        ),
    ]
