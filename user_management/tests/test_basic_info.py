from django.test import TestCase
from user_management.models import group_info, all_permissions
from django.contrib.auth.models import User, Group
import datetime


class UserInfoTestCase(TestCase):

    @classmethod
    def setUpTestCase(cls):
        pass

    def setUp(self):
        user, created = User.objects.get_or_create(username='u_test_basic_info')
        group, created = Group.objects.get_or_create(name='Public')
        user.basicinfo.date_of_birth = datetime.datetime.now().date()
        user.basicinfo.contact_number = '2929292929'
        user.basicinfo.group = group
        user.save()

    def test_contact_number(self):
        user = User.objects.get(username='u_test_basic_info')
        self.assertEquals(user.basicinfo.contact_number, '2929292929')

    def test_date_of_birth(self):
        user = User.objects.get(username='u_test_basic_info')
        self.assertEquals(
            user.basicinfo.date_of_birth, datetime.datetime.now().date())

    def test_basic_info_reverse_url(self):
        user = User.objects.get(username='u_test_basic_info')
        url = user.basicinfo.get_absolute_url()
        self.assertEquals(url, '/user_management/' + str(user.pk) + "/")