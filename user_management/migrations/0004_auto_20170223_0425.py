# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 22:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0003_auto_20170223_0050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='allpermissions',
            options={'default_permissions': (), 'managed': False, 'permissions': set([('can_write_fee_dues', 'can write fee dues'), ('can_read_notices', 'can read notices'), ('can_read_attendance', 'can read attendance'), ('can_write_id_card_req', 'can write id card req'), ('can_write_rail_pass_req', 'can write rail pass req'), ('can_write_internal_assessment', 'can write internal assessment'), ('can_read_fee_collections', 'can read fee collections'), ('can_read_assignments', 'can read assignments'), ('can_read_pass_my_book', 'can read pass my book'), ('can_read_library_card_req', 'can read library card req'), ('can_write_attendance', 'can write attendance'), ('can_write_meeting_details', 'can write meeting details'), ('can_write_activity_log', 'can write activity log'), ('can_auth_accounts_library', 'can auth accounts_library'), ('can_read_exam_schedule', 'can read exam schedule'), ('can_write_pass_my_book', 'can write pass my book'), ('can_write_personal_profile', 'can write personal profile'), ('can_write_exam_hall_plan', 'can write exam hall plan'), ('can_write_exam_schedule', 'can write exam schedule'), ('can_write_online_discussion', 'can write online discussion'), ('can_read_activity_log', 'can read activity log'), ('can_write_study_materials', 'can write study materials'), ('can_read_study_materials', 'can read study materials'), ('can_read_online_discussion', 'can read online discussion'), ('can_read_exam_hall_plan', 'can read exam hall plan'), ('can_read_time_table', 'can read time table'), ('can_read_meeting_details', 'can read meeting details'), ('can_read_internal_assessment', 'can read internal assessent'), ('can_read_id_card_req', 'can read id card req'), ('can_read_university_credits', 'can read university credits'), ('can_auth_sub_admin', 'can auth sub_admin'), ('can_read_main_page', 'can read main page'), ('can_read_rail_pass_req', 'can read rail pass req'), ('can_write_fee_collections', 'can write fee collections'), ('can_write_bonafide_req', 'can write bonafide req'), ('can_authenticate_users', 'can authenticate users'), ('can_write_assignments', 'can write assignments'), ('can_read_fee_dues', 'can read fee dues'), ('can_write_notices', 'can write notices'), ('can_write_library_card_req', 'can write library card req'), ('can_write_time_table', 'can write time table'), ('can_auth_students', 'can auth students'), ('can_write_university_credits', 'can write university credits'), ('can_read_bonafide_req', 'can read bonafide req'), ('can_auth_faculty', 'can auth faculty')])},
        ),
    ]
