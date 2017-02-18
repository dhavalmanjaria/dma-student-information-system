# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 21:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0011_auto_20170218_0200'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LibraryInfo',
            new_name='AdminInfo',
        ),
        migrations.RemoveField(
            model_name='accountsinfo',
            name='user',
        ),
        migrations.RemoveField(
            model_name='subadmininfo',
            name='user',
        ),
        migrations.DeleteModel(
            name='AccountsInfo',
        ),
        migrations.DeleteModel(
            name='SubAdminInfo',
        ),
    ]
