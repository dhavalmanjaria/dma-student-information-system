from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from permission_structure.management.commands import initgroups
from permission_structure.models import AllPermissions


class GroupPermissionsTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cmd = initgroups.Command()
        cmd.handle()

    def setUp(self):
        global cmd
        cmd = initgroups.Command()

    def testPublic(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='Public').permissions.all()])

        role_perms = cmd._getPerms('Public')

        self.assertEquals(group_perms, role_perms)

    def testPermsMatchModel(self):
        model_perms = set()
        for p in AllPermissions._meta.permissions:
            model_perms.add(p[0])

        role_perms = set()
        for k, v in initgroups.PERMISSIONS_BY_ROLE.items():
            for p in v:
                role_perms.add(p)

        self.assertEquals(model_perms, role_perms)

    def testGenericUserAcademic(self):
        group_perms = set([perm.codename for perm in Group.objects.get(
                          name='GenericUserAcademic').permissions.all()])

        role_perms = cmd._getPerms('GenericUserAcademic')
        self.assertEquals(group_perms, role_perms)

    def testGenericUserAdministrative(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='GenericUserAdministrative').permissions.all()])

        role_perms = cmd._getPerms('GenericUserAdministrative')
        self.assertEquals(group_perms, role_perms)

    def testStudent(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='Student').permissions.all()])

        role_perms = cmd._getPerms('Student')
        self.assertEquals(group_perms, role_perms)

    def testFaculty(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='Faculty').permissions.all()])

        role_perms = cmd._getPerms('Faculty')
        self.assertEquals(group_perms, role_perms)

    def testFacultyHOD(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='FacultyHOD').permissions.all()])

        role_perms = cmd._getPerms('FacultyHOD')
        self.assertEquals(group_perms, role_perms)

    def testSubAdmin(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='SubAdmin').permissions.all()])

        role_perms = cmd._getPerms('SubAdmin')
        self.assertEquals(group_perms, role_perms)

    def testAccounts(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='Accounts').permissions.all()])

        role_perms = cmd._getPerms('Accounts')
        self.assertEquals(group_perms, role_perms)

    def testLibrary(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='Library').permissions.all()])

        role_perms = cmd._getPerms('Library')
        self.assertEquals(group_perms, role_perms)

    def testUpperManagement(self):
        group_perms = set([perm for perm in Group.objects.get(
                          name='UpperManagement').permissions.all()])

        role_perms = cmd._getPerms('UpperManagement')
        self.assertEquals(group_perms, role_perms)
