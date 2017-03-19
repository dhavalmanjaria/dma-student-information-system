from django.test import TestCase
from django.contrib.auth.models import User, Group
from user_management.management.commands import initgroups, createumuser
from curriculum.management.commands import initcurriculum
from curriculum.models import Semester, Subject
from internal_assessment.models import Metric
from university_credits.models import SubjectCredit
from university_credits.management.commands import initcredits
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
        cmd = initcredits.Command()
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

    #TO MOVE, maybe
    def test_new_user_has_no_metrics(self):
        data = {
            'username': 'u_test_new_user_has_no_metrics',
            'email': 'dhv2712@gmail.com',
            'password1': 'dhaval27',
            'password2': 'dhaval27',
            'date_of_birth': '22/7/1989',
            'contact_number': '9881585223',
            'group': Group.objects.get(name='Student').pk,
            'semester': Semester.objects.get(
                course__short_name='BCA', semester_number=2).pk
        }

        resp = self.client.post(
            '/user_management/register/new.html', data=data)

        user = User.objects.get(username='u_test_new_user_has_no_metrics')

        smetrics = user.studentinfo.studentmetric_set.all()

        self.assertTrue(len(smetrics) == 0)

    def test_new_user_has_metrics(self):

        # Create metrics for any one subject
        subject = Subject.objects.get(name='SSAD')
        metric = Metric.objects.get_or_create(
            name='assignment', subject=subject, max_marks=10)

        data = {
            'username': 'u_test_new_user_has_metrics',
            'email': 'dhv2712@gmail.com',
            'password1': 'dhaval27',
            'password2': 'dhaval27',
            'date_of_birth': '22/7/1989',
            'contact_number': '9881585223',
            'group': Group.objects.get(name='Student').pk,
            'semester': Semester.objects.get(
                course__short_name='BCA', semester_number=2).pk
        }

        self.client.post(
            '/user_management/register/new.html', data=data)

        user = User.objects.get(username='u_test_new_user_has_metrics')
        ar = AuthenticationRequest.objects.get(user=user)

        self.client.login(username='um0', password='dhaval27')

        self.client.post('/actions/grant_request/', {'pk': ar.pk},
                         follow=True)


        smetrics = user.studentinfo.studentmetric_set.all()

        self.assertTrue(len(smetrics) > 0)


    def test_new_user_has_credits(self):
        # subject = Subject.objects.get(name='SSAD')
        # credit = SubjectCredit.objects.get_or_create(subject=subject)

        data = {
            'username': 'u_test_new_user_has_credits',
            'email': 'dhv2712@gmail.com',
            'password1': 'dhaval27',
            'password2': 'dhaval27',
            'date_of_birth': '22/7/1989',
            'contact_number': '9881585223',
            'group': Group.objects.get(name='Student').pk,
            'semester': Semester.objects.get(
                course__short_name='BCA', semester_number=2).pk
        }

        self.client.post(
            '/user_management/register/new.html', data=data)

        user = User.objects.get(username='u_test_new_user_has_credits')
        ar = AuthenticationRequest.objects.get(user=user)

        self.client.login(username='um0', password='dhaval27')

        self.client.post('/actions/grant_request/', {'pk': ar.pk},
                         follow=True)


        ucrd = user.studentinfo.universitycredit_set.all()
        
        self.assertTrue(len(ucrd) > 0)

