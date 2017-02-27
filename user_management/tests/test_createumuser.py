from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission
from user_management.management.commands import createumuser, initgroups


class UMUserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cmd = initgroups.Command()
        cmd.handle()
        cmd = createumuser.Command()
        cmd.handle()

    def test_um0_exists(self):
        um0 = User.objects.get(username='um0')
        self.assertTrue(um0 is not None)

    def test_um0_details(self):
        um0 = User.objects.get(username='um0')
        self.assertTrue(um0.first_name == "UM")
        self.assertTrue(um0.last_name == "User")
        self.assertTrue(um0.basicinfo.group == Group.objects.get(
            name="UpperManagement"))

    def test_um0_perms(self):
        group_perms = [p for p in Group.objects.get(
            name="UpperManagement").permissions.all()]
        um0 = User.objects.get(username='um0')
        um0_perms = [p for p in um0.user_permissions.all()]
        self.assertEquals(group_perms, um0_perms)
