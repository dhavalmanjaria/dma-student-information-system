# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 19:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0002_subject_faculty'),
        ('university_credits', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectCredit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_credits', models.IntegerField(default=0)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum.Subject')),
            ],
        ),
        migrations.RemoveField(
            model_name='universitycredit',
            name='credits',
        ),
        migrations.RemoveField(
            model_name='universitycredit',
            name='max_credits',
        ),
        migrations.RemoveField(
            model_name='universitycredit',
            name='student',
        ),
        migrations.RemoveField(
            model_name='universitycredit',
            name='subject',
        ),
        migrations.AlterUniqueTogether(
            name='subjectcredit',
            unique_together=set([('subject', 'max_credits')]),
        ),
    ]