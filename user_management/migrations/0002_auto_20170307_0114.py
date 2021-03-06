# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 19:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0001_initial'),
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectFaculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.FacultyInfo')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum.Subject')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='subjectfaculty',
            unique_together=set([('subject', 'faculty')]),
        ),
    ]
