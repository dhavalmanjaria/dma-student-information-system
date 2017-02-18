from django.test import TestCase
from django.contrib.auth.models import Group, User
from user_management.forms import UserForm, BasicInfoForm, StudentInfoForm
from user_management.models.curriculum import Semester, Course


class RegistrationViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        group, created = Group.objects.get_or_create(name='Public')
        group, created = Group.objects.get_or_create(name='GUAc')
        group, created = Group.objects.get_or_create(name='GUAd')
        group, created = Group.objects.get_or_create(name='Student')
        course, created = Course.objects.get_or_create(short_name='CCP')
        sem, created = Semester.objects.get_or_create(
            course=course, semester_number=2)

    def setUp(self):
        pass

    def test_url(self):
        resp = self.client.get('/user_management/register/new.html')
        self.assertEqual(resp.status_code, 200)

    def test_user_form_is_table(self):
        user_form = UserForm()
        resp = self.client.get('/user_management/register/new.html')
        self.assertEqual(user_form.as_table(), resp.context['user_form'])

    def test_basic_info_form_is_table(self):
        basic_info = BasicInfoForm()
        resp = self.client.get('/user_management/register/new.html')
        self.assertEqual(
            basic_info.as_table(), resp.context['basic_info_form'])

    def test_second_form_is_student(self):
        second_form = StudentInfoForm()
        resp = self.client.get('/user_management/register/new.html?option=3')
        self.assertEqual(second_form.as_table().encode(), resp.content)

    def test_second_form_success(self):
        data = {
            'username': 'test_user',
            'email': 'dhv2712@gmail.com',
            'password1': 'dhaval27',
            'password2': 'dhaval27',
            'date_of_birth': '22/7/1989',
            'contact_number': '9881585223',
            'group': '4',
            'semester': '1'
        }
        resp = self.client.post(
            '/user_management/register/new.html', data=data)
        print(resp.content)
        self.assertTrue('SUCCESS'.encode() in resp.content)

    def test_second_form_adds_semester(self):
        data = {
            'username': 'test_user_with_sem',
            'email': 'dhv2712@gmail.com',
            'password1': 'dhaval27',
            'password2': 'dhaval27',
            'date_of_birth': '22/7/1989',
            'contact_number': '9881585223',
            'group': '4',
            'semester': '1'
        }
        resp = self.client.post(
            '/user_management/register/new.html', data=data)
        test_user = User.objects.get(username='test_user_with_sem')
        self.assertEquals(test_user.studentinfo.semester.semester_number, 2)
