from django.test import TestCase
from django.contrib.auth.models import User, Group
from user_management.management.commands import initgroups, createumuser
from curriculum.management.commands import initcurriculum
from user_management.models.auth_requests import AuthenticationRequest
from datetime import datetime
from django.contrib.auth import login, authenticate
import logging

LOG = logging.getLogger('app')


class AuthenticationRequestTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cmd = initgroups.Command()
        cmd.handle()
        cmd = createumuser.Command()
        cmd.handle()
        cmd = initcurriculum.Command()
        cmd.handle()


    def test_save_request(self):
        data = {
            'username': 'u_test_save_request',
            'email': 'dhv2712@gmail.com',
            'password1': 'dhaval27',
            'password2': 'dhaval27',
            'date_of_birth': '22/7/1989',
            'contact_number': '9881585223',
            'group': Group.objects.get(name='Student').pk,
            'semester': '1'
        }

        resp = self.client.post(
            '/user_management/register/new.html', data=data)

        user = User.objects.get(username='u_test_save_request')

        ar = AuthenticationRequest.objects.get(user=user)

        self.assertTrue(ar is not None)

    def test_ar_date(self):
        data = {
            'username': 'u_test_ar_date',
            'email': 'dhv2712@gmail.com',
            'password1': 'dhaval27',
            'password2': 'dhaval27',
            'date_of_birth': '22/7/1989',
            'contact_number': '9881585223',
            'group': Group.objects.get(name='Student').pk,
            'semester': '1'
        }

        resp = self.client.post(
            '/user_management/register/new.html', data=data)

        user = User.objects.get(username='u_test_ar_date')

        ar = AuthenticationRequest.objects.get(user=user)

        self.assertEquals(ar.request_date, datetime.now().date())

    def test_grant_request(self):
        data = {
            'username': 'u_test_grant_request',
            'email': 'dhv2712@gmail.com',
            'password1': 'dhaval27',
            'password2': 'dhaval27',
            'date_of_birth': '22/7/1989',
            'contact_number': '9881585223',
            'group': Group.objects.get(name='Student').pk,
            'semester': '1'
        }

        resp = self.client.post(
            '/user_management/register/new.html', data=data)

        user = User.objects.get(username='u_test_grant_request')

        ar = AuthenticationRequest.objects.get(user=user)
        self.client.login(username='um0', password='dhaval27')

        self.client.post('/actions/grant_request/', {'pk': ar.pk},
                         follow=True)
        ar = AuthenticationRequest.objects.get(user=user)
        
        self.assertTrue(ar.is_approved)

    def test_new_user_has_perms(self):
        data = {
            'username': 'u_test_new_user_has_perms',
            'email': 'dhv2712@gmail.com',
            'password1': 'dhaval27',
            'password2': 'dhaval27',
            'date_of_birth': '22/7/1989',
            'contact_number': '9881585223',
            'group': Group.objects.get(name='Student').pk,
            'semester': '1'
        }

        resp = self.client.post(
            '/user_management/register/new.html', data=data)

        user = User.objects.get(username='u_test_new_user_has_perms')

        ar = AuthenticationRequest.objects.get(user=user)
        self.client.login(username='um0', password='dhaval27')

        self.client.post('/actions/grant_request/', {'pk': ar.pk},
                         follow=True)

        group = Group.objects.get(name='Student')

        group_perms = [p.codename for p in group.permissions.all()]

        user_perms = [p.codename for p in user.user_permissions.all()]

        self.assertEquals(group_perms, user_perms)