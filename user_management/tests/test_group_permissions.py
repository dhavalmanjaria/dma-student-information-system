from django.test import TestCase
from django.contrib.auth.models import Group
from user_management.management.commands import initgroups
# from user_management.models.all_permissions import AllPermissions


class GroupPermissionsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        global cmd
        cmd = initgroups.Command()
        cmd.handle()

    def setUp(self):
        pass

    def testPublic(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='Public').permissions.all()])

        role_perms = cmd._getPerms('Public')

        self.assertEquals(group_perms, role_perms)

    def testGenericUserAcademic(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='GenericUserAcademic').permissions.all()])

        role_perms = cmd._getPerms('GenericUserAcademic')
        role_perms = role_perms.union(set(
            Group.objects.get(name='Public').permissions.all()))
        self.assertEquals(group_perms, role_perms)

    def testGenericUserAdministrative(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='GenericUserAdministrative').permissions.all()])

        role_perms = cmd._getPerms('GenericUserAdministrative')
        role_perms = role_perms.union(set(
            Group.objects.get(name='Public').permissions.all()))
        self.assertEquals(group_perms, role_perms)

    def testStudent(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='Student').permissions.all()])

        role_perms = cmd._getPerms('Student')
        role_perms = role_perms.union(set(
            Group.objects.get(name='GenericUserAcademic').permissions.all()))
        self.assertEquals(group_perms, role_perms)

    def testFaculty(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='Faculty').permissions.all()])

        role_perms = cmd._getPerms('Faculty')
        role_perms = role_perms.union(set(
            Group.objects.get(name='GenericUserAcademic').permissions.all()))
        
        self.assertEquals(group_perms, role_perms)

    def testFacultyHOD(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='FacultyHOD').permissions.all()])

        role_perms = cmd._getPerms('FacultyHOD')
        role_perms = role_perms.union(set(
            Group.objects.get(name='Faculty').permissions.all()))
        self.assertEquals(group_perms, role_perms)

    def testSubAdmin(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='SubAdmin').permissions.all()])

        role_perms = cmd._getPerms('SubAdmin')
        role_perms = role_perms.union(set(
            Group.objects.get(
                name='GenericUserAdministrative').permissions.all()))
        self.assertEquals(group_perms, role_perms)

    def testAccounts(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='Accounts').permissions.all()])

        role_perms = cmd._getPerms('Accounts')
        role_perms = role_perms.union(set(
            Group.objects.get(
                name='GenericUserAdministrative').permissions.all()))

        self.assertEquals(group_perms, role_perms)

    def testLibrary(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='Library').permissions.all()])

        role_perms = cmd._getPerms('Library')
        role_perms = role_perms.union(set(
            Group.objects.get(
                name='GenericUserAdministrative').permissions.all()))

        self.assertEquals(group_perms, role_perms)

    def testUpperManagement(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='UpperManagement').permissions.all()])

        role_perms = cmd._getPerms('UpperManagement')
        role_perms = role_perms.union(set(
            Group.objects.get(
                name='SubAdmin').permissions.all()))
        role_perms = role_perms.union(set(
            Group.objects.get(
                name='Accounts').permissions.all()))
        role_perms = role_perms.union(set(
            Group.objects.get(
                name='FacultyHOD').permissions.all()))

        self.assertEquals(group_perms, role_perms)
