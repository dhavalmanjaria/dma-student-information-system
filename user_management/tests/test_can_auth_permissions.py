from django.test import TestCase
from django.contrib.auth.models import Group, User
from curriculum.models import Semester, Course
from user_management.management.commands import initgroups, createumuser
from curriculum.management.commands import initcurriculum


class CanAuthTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cmd = initgroups.Command()
        cmd.handle()
        cmd = createumuser.Command()
        cmd.handle()

    def test_can_auth_perms(self):
        """
        This tests test that can_auth_<group_name> returns the proper group
        names
        """
        user = User.objects.get(username='um0')

        can_auth_perms = [p.codename for p in user.user_permissions.filter(
            codename__startswith='can_auth_')]

        can_auth_groups = [n.replace('can_auth_', '') for n in can_auth_perms]

        for g in can_auth_groups:
            group = Group.objects.get(name=g)
            self.assertTrue(group is not None)




