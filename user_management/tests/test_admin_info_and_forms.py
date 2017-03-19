from django.test import TestCase
from user_management.management.commands import initgroups, createumuser


class AdminInfoTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cmd = initgroups.Command()
        cmd.handle()
        cmd = createumuser.Command()
        cmd.handle()
        global test_user
        group, created = Group.objects.get_or_create(name='Accounts')
        test_user, created = User.objects.get_or_create(username='u_test_admin')
        test_user.basicinfo.date_of_birth = datetime.datetime.now().date()
        test_user.basicinfo.contact_number = '2929292929'
        test_user.basicinfo.group = group
        test_user.save()

    def test_account_group(self):

