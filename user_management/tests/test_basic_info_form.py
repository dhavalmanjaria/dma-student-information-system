from django.test import TestCase

from user_management.forms import UserForm, BasicInfoForm, StudentInfoForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import check_password
from datetime import datetime
from user_management.management.commands import initgroups
import logging

LOG = logging.getLogger('app')


class BasicInfoFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cmd = initgroups.Command()
        cmd.handle()

    def setUp(self):
        form_data = {
            'username': 'u_test_basic_info_form',
            'password1': 'dhaval27',
            'password2': 'dhaval27',
            'email': 'mail@dhaval.com'
        }
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())
        LOG.debug(form.errors)
        u = form.save()

        form_data = {
            'date_of_birth': '22/7/89',
            'contact_number': '9881585223',
            'group': Group.objects.get(name='Student').pk
        }
        form = BasicInfoForm(data=form_data, instance=u)
        self.assertTrue(form.is_valid())
        LOG.debug(form.errors)
        u = form.save()

    def test_basic_info_exists(self):
        test_user = User.objects.get(username='u_test_basic_info_form')
        self.assertTrue(test_user.basicinfo is not None)

    def test_basic_info_save(self):
        test_user = User.objects.get(username='u_test_basic_info_form')
        form_data = {
            'date_of_birth': '22/7/89',
            'contact_number': '9881585223',
            'group': Group.objects.get(name='Student').pk
        }
        form = BasicInfoForm(data=form_data, instance=test_user)
        self.assertTrue(form.is_valid())
        form.save()

    def test_date_of_birth(self):
        test_user = User.objects.get(username='u_test_basic_info_form')
        dob = test_user.basicinfo.date_of_birth
        entered_dob = datetime(1989, 7, 22).date()
        self.assertEqual(dob, entered_dob)

    def test_contact_number(self):
        test_user = User.objects.get(username='u_test_basic_info_form')
        self.assertEqual(
            test_user.basicinfo.contact_number, '9881585223')

    def tearDown(self):
        Group.objects.all().delete()
