# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-05 22:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the Notice', max_length=255)),
                ('priority', models.CharField(choices=[('1', 'Very Important'), ('2', 'Important'), ('3', 'General')], max_length=1)),
                ('date', models.DateField(auto_now=True)),
                ('addressed_to', models.CharField(help_text='Everyone that the notice is applies to', max_length=255)),
                ('text', models.TextField()),
                ('other_details', models.TextField()),
                ('signed_by', models.CharField(max_length=255)),
            ],
        ),
    ]
