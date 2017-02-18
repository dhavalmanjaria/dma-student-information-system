from django.test import TestCase

from user_management.forms import UserForm, BasicInfoForm, StudentInfoForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import check_password


class UserFormTest(TestCase):
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

        global test_user
        test_user = u

    def test_test(self):
        self.assertTrue(True)
    
    def test_user_name(self):
        self.assertEquals(test_user.username, 'test_u1a')

    def test_user_password(self):
        # form_data = {
        #     'username': 'test_u1a',
        #     'password1': 'dhaval27',
        #     'password2': 'dhaval27',
        #     'email': 'mail@dhaval.com'
        # }
        # form = UserForm(data=form_data)
        # u = form.save()
        u = User.objects.get(username='test_u1a')
        self.assertTrue(check_password('dhaval27', u.password))

    def test_user_email(self):
        self.assertEquals(test_user.email, 'mail@dhaval.com')
