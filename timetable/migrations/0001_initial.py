# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 15:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('curriculum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], help_text='Day of week as per date.isoweekday()')),
                ('start_time', models.CharField(help_text='Start time in 24h format (easier to work with this way', max_length=4)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum.Semester')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum.Subject')),
            ],
        ),
    ]
