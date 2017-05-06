# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-05 18:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_management', '0009_auto_20170307_2039'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeeCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pending_amount', models.IntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.StudentInfo')),
            ],
        ),
        migrations.CreateModel(
            name='FeeItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(help_text='Name of the fee item with a fixed amount', max_length=200)),
                ('item_amount', models.IntegerField()),
            ],
        ),
    ]
