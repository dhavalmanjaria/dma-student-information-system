from django.test import TestCase
from user_management import models
from django.contrib.auth.models import User
import datetime


class BasicInfoTestCase(TestCase):

    @classmethod
    def setUpTestCase(cls):
        pass
        
    def setUp(self):
        user, created = User.objects.get_or_create(username='new_user')
        user.basicinfo.date_of_birth = datetime.datetime.now().date()
        user.basicinfo.contact_number = '2929292929'
        user.save()

    def test_contact_number(self):
        user = User.objects.get(username='new_user')
        self.assertEquals(user.basicinfo.contact_number, '2929292929')

    def test_date_of_birth(self):
        user = User.objects.get(username='new_user')
        self.assertEquals(
            user.basicinfo.date_of_birth, datetime.datetime.now().date())
