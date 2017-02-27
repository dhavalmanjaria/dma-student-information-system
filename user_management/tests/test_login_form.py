from django.test import TestCase
from django.contrib.auth.models import User, Group
from user_management.management.commands import initgroups, createumuser
from django.contrib.auth.hashers import make_password


class LoginFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cmd = initgroups.Command()
        cmd.handle()
        global user
        user = User.objects.create(username='u_test_login_form')
        user.password = make_password('dhaval27')
        user.save()

    def test_profile_redirect(self):
        global user
        login_data = {
            'username': 'u_test_login_form',
            'password': 'dhaval27'
        }
        resp = self.client.post('/user_management/accounts/profile/',
                                data=login_data)

        self.assertEquals(resp.status_code, 302)

    def test_login_success(self):
        global user
        login_data = {
            'username': 'u_test_login_form',
            'password': 'dhaval27'
        }
        resp = self.client.post('/user_management/accounts/profile/',
                                data=login_data)

        self.assertEquals(resp.url, '/user_management/' + str(user.pk) + '/')

    def test_login_fail(self):
        global user
        login_data = {
            'username': 'u_test_login_form_fail',
            'password': 'dhaval27'
        }
        resp = self.client.post('/user_management/accounts/profile/',
                                data=login_data)

        self.assertEquals(resp.url, '/user_management/accounts/login/')
