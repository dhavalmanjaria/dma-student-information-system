from django.test import TestCase

from user_management.forms import UserForm, BasicInfoForm, StudentInfoForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import check_password
from datetime import datetime


class BasicInfoFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        group, created = Group.objects.get_or_create(name='Public')
        print("Group.pk: " + str(group.pk))

    def setUp(self):
        form_data = {
            'username': 'test_u1a',
            'password1': 'dhaval27',
            'password2': 'dhaval27',
            'email': 'mail@dhaval.com'
        }
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())
        u = form.save()

        form_data = {
            'date_of_birth': '22/7/89',
            'contact_number': '9881585223',
            'group': 1
        }
        form = BasicInfoForm(data=form_data, instance=u)
        self.assertTrue(form.is_valid())
        form.save()

        global test_user
        test_user = u

    def test_test(self):
        self.assertTrue(True)

    def test_basic_info_exists(self):
        self.assertTrue(test_user.basicinfo is not None)

    def test_basic_info_save(self):
        form_data = {
            'date_of_birth': '22/7/89',
            'contact_number': '9881585223',
            'group': 1
        }
        form = BasicInfoForm(data=form_data, instance=test_user)
        self.assertTrue(form.is_valid())
        form.save()

    def test_date_of_birth(self):
        dob = test_user.basicinfo.date_of_birth
        entered_dob = datetime(1989, 7, 22).date()
        self.assertEqual(dob, entered_dob)

    def test_contact_number(self):
        self.assertEqual(
            test_user.basicinfo.contact_number, '9881585223')