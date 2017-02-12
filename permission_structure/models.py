from django.db import models

"""
The roles described here only carry a specific set of permissions
This means that each role only carries permissions that it adds to the
hierarchy. The Inheritance structure, is implemented in the groups.
Groups inherit permissions from other groups mostly. It is recommended
that this functionality be abstracted away so it can done via the UI.
However, in any case, it can only be done manually.
"""


class AllPermissions(models.Model):
    """
    Represents all the permissions that are available for Roles
    """
    class Meta:
        managed = False
        default_permissions = ()
        permissions = set((
                      ('can_read_main_page', 'can read main page'),
                      ('can_read_notices', 'can read notices'),
                      ('can_read_study_materials', 'can read study materials'),
                      ('can_read_time_table', 'can read time table'),
                      ('can_read_assignments', 'can read assignments'),
                      ('can_read_exam_schedule', 'can read exam schedule'),
                      ('can_read_exam_hall_plan', 'can read exam hall plan'),

                      ('can_write_personal_profile',
                       'can write personal profile'),

                      ('can_read_attendance',
                       'can read attendance'),

                      ('can_read_university_credits',
                       'can read university credits'),

                      ('can_read_online_discussion',
                       'can read online discussion'),

                      ('can_write_online_discussion',
                       'can write online discussion'),

                      ('can_read_activity_log',
                       'can read activity log'),

                      ('can_read_internal_assessment',
                       'can read internal assessent'),

                      ('can_write_study_materials',
                       'can write study materials'),

                      ('can_read_fee_dues',
                       'can read fee dues'),

                      ('can_write_fee_dues',
                       'can write fee dues'),

                      ('can_read_fee_collections',
                       'can read fee collections'),

                      ('can_write_fee_collections',
                       'can write fee collections'),

                      ('can_read_id_card_req',
                       'can read id card req'),

                      ('can_write_id_card_req',
                       'can write id card req'),

                      ('can_read_library_card_req',
                       'can read library card req'),

                      ('can_write_library_card_req',
                       'can write library card req'),

                      ('can_read_pass_my_book',
                       'can read pass my book'),

                      ('can_write_pass_my_book',
                       'can write pass my book'),

                      ('can_read_rail_pass_req',
                       'can read rail pass req'),

                      ('can_write_rail_pass_req',
                       'can write rail pass req'),

                      ('can_read_bonafide_req',
                       'can read bonafide req'),

                      ('can_write_bonafide_req',
                       'can write bonafide req'),

                      ('can_write_notices',
                       'can write notices'),

                      ('can_write_attendance',
                       'can write attendance'),

                      ('can_write_internal_assessment',
                       'can write internal assessment'),

                      ('can_write_assignments',
                       'can write assignments'),

                      ('can_write_activty_log',
                       'can write activty log'),

                      ('can_read_meeting_details',
                       'can read meeting details'),

                      ('can_authenticate_users',
                       'can authenticate users'),

                      ('can_write_time_table',
                       'can write time table'),

                      ('can_write_university_credits',
                       'can write university credits'),

                      ('can_write_meeting_details',
                       'can write meeting details'),

                      ('can_write_exam_schedule',
                       'can write exam schedule'),

                      ('can_write_exam_hall_plan',
                       'can write exam hall plan'),

                      ('can_read_pass_my_book',
                       'can read pass my book'),

                      ('can_write_pass_my_book',
                       'can write pass my book')
                    ))
