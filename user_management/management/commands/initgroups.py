# Copyright Dhaval Anjaria 2017
#
# This file is part of DMA Student Information System.
# DMA Student Information System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# DMA Student Information System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with DMA Student Information System.  If not, see <http://www.gnu.org/licenses/>.

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
import logging

LOG = logging.getLogger('app')

PERMISSIONS_BY_ROLE = {
    'Public': (('can_read_main_page'),
               ('can_read_notices'),
               ('can_read_study_materials'),
               ('can_read_time_table'),
               ('can_read_assignments'),
               ('can_read_exam_schedule'),
               ('can_read_exam_hall_plan')),

    'GenericUserAcademic': (('can_write_personal_profile'),
                            ('can_read_attendance'),
                            ('can_read_online_discussion'),
                            ('can_read_activity_log'),
                            ('can_read_internal_assessment'),
                            ('can_write_study_materials'),
                            ('can_read_university_credits'),
                            ('can_write_online_discussion')),

    'GenericUserAdministrative': (('can_read_exam_hall_plan'),
                                  ('can_read_fee_dues'),
                                  ('can_read_id_card_req'),
                                  ('can_write_id_card_req'),
                                  ('can_read_rail_pass_req'),
                                  ('can_write_rail_pass_req'),
                                  ('can_read_bonafide_req'),
                                  ('can_read_bonafide_req')),

    'Student': (('can_write_pass_my_book'),
                ('can_write_id_card_req'),
                ('can_write_library_card_req'),
                ('can_write_rail_pass_req'),
                ('can_write_bonafide_req')),

    'Faculty': (('can_write_notices'),
                ('can_write_attendance'),
                ('can_write_internal_assessment'),
                ('can_write_assignments'),
                ('can_write_activity_log'),
                ('can_read_meeting_details'),
                ('can_auth_Student')),

    'SubAdmin': (('can_write_activity_log'),
                 ('can_write_exam_hall_plan'),
                 ('can_read_fee_collections'),
                 ('can_auth_SubAdmin'),
                 ('can_auth_Accounts'),
                 ('can_auth_Library')),

    'Accounts': (('can_read_fee_collections'),
                 ('can_write_fee_collections'),
                 ('can_write_fee_dues')),

    'Library': (('can_read_pass_my_book'),
                ('can_write_pass_my_book'),
                ('can_read_library_card_req'),
                ('can_write_library_card_req')),

    'FacultyHOD': (('can_write_time_table'),
                   ('can_write_university_credits'),
                   ('can_write_meeting_details'),
                   ('can_write_exam_schedule'),
                   ('can_write_exam_hall_plan'),
                   ('can_auth_Faculty'),
                   ('can_write_subject_faculty')),

    'UpperManagement': (('can_read_pass_my_book'),
                        ('can_write_pass_my_book'),
                        ('can_read_id_card_req'),
                        ('can_auth_FacultyHOD'),
                        ('can_write_all_internal_assessment'),
                        ('can_write_all_assignments'))
}


class Command(BaseCommand):
    """
    Command Class. This command will initialize all the groups in the system
    and imbue them with the relavant permissions
    """

    help = 'Initialize the permissions hierarchy for all groups'

    def _getPerms(self, groupname):
        perms = set()
        for p in PERMISSIONS_BY_ROLE[groupname]:
            current_perm = Permission.objects.filter(codename=p).first()
            if groupname == "UpperManagement":
                LOG.debug("_getPerm: Adding " + current_perm.codename)
            perms.add(current_perm)

        return perms

    def _setPermissionsForGroup(self, groupname, inherited_groups=[],
                                additional_perms=set()):
        group, created = Group.objects.get_or_create(name=groupname)

        for g in inherited_groups:
            for p in Group.objects.get(name=g).permissions.all():
                additional_perms.add(p)

        # LOG.debug("GROUPNAME: " + groupname)
        # for p in additional_perms:
            # LOG.debug(p)
        group.permissions.set(additional_perms)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
        Function that executes the command
        """

        # Public user
        self._setPermissionsForGroup(
            groupname='Public', additional_perms=self._getPerms('Public'))

        # Generic User Academic
        self._setPermissionsForGroup(
            groupname='GenericUserAcademic',
            inherited_groups=['Public'],
            additional_perms=self._getPerms('GenericUserAcademic'))

        # Generic User Administrative
        self._setPermissionsForGroup(
            groupname='GenericUserAdministrative',
            inherited_groups=['Public'],
            additional_perms=self._getPerms('GenericUserAdministrative'))

        # Student
        self._setPermissionsForGroup(
            groupname='Student',
            inherited_groups=['GenericUserAcademic'],
            additional_perms=self._getPerms('Student'))

        # Faculty
        self._setPermissionsForGroup(
            groupname='Faculty',
            inherited_groups=['GenericUserAcademic'],
            additional_perms=self._getPerms('Faculty'))

        # FacultyHOD
        self._setPermissionsForGroup(
            groupname='FacultyHOD',
            inherited_groups=['Faculty'],
            additional_perms=self._getPerms('FacultyHOD'))

        # SubAdmin
        self._setPermissionsForGroup(
            groupname='SubAdmin',
            inherited_groups=['GenericUserAdministrative'],
            additional_perms=self._getPerms('SubAdmin'))

        # Accounts
        self._setPermissionsForGroup(
            groupname='Accounts',
            inherited_groups=['GenericUserAdministrative'],
            additional_perms=self._getPerms('Accounts'))

        # Library
        self._setPermissionsForGroup(
            groupname='Library',
            inherited_groups=['GenericUserAdministrative'],
            additional_perms=self._getPerms('Library'))

        # UpperManagement
        self._setPermissionsForGroup(
            groupname='UpperManagement',
            inherited_groups=['FacultyHOD', 'SubAdmin', 'Accounts'],
            additional_perms=self._getPerms('UpperManagement'))

