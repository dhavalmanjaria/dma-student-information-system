# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('examinations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='academic_year',
            field=models.IntegerField(default=2017, help_text='Year that the academic year started in.'),
        ),
        migrations.AlterUniqueTogether(
            name='exam',
            unique_together=set([('exam_name', 'academic_year')]),
        ),
    ]
