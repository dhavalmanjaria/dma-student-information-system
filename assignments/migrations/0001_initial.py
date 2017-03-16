# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 06:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('curriculum', '0002_subject_faculty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('due_date', models.DateField()),
                ('description', models.TextField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum.Subject')),
            ],
        ),
    ]