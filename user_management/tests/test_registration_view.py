from django.test import TestCase
from django.contrib.auth.models import Group, User
from user_management.forms import UserForm, BasicInfoForm, StudentInfoForm, FacultyInfoForm
from user_management.models.curriculum import Semester, Course


class RegistrationViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        group, created = Group.objects.get_or_create(name='Public')
        group, created = Group.objects.get_or_create(name='GUAc')
        group, created = Group.objects.get_or_create(name='GUAd')
        group, created = Group.objects.get_or_create(name='Student')
        group, created = Group.objects.get_or_create(name='Faculty')
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
        self.assertEqual(user_form.as_ul(), resp.context['user_form'])

    def test_basic_info_form_is_table(self):
        basic_info = BasicInfoForm()
        resp = self.client.get('/user_management/register/new.html')
        self.assertEqual(
            basic_info.as_ul(), resp.context['basic_info_form'])

    def test_second_form_is_student(self):
        second_form = StudentInfoForm()
        resp = self.client.get(
            '/user_management/register/new.html?group=' + str(
                Group.objects.get(name='Student').pk),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(second_form.as_ul().encode(), resp.content)

    def test_second_form_student_success(self):
        data = {
            'username': 'u_test_registration_view',
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
        self.assertTrue('SUCCESS'.encode() in resp.content)

    def test_second_form_adds_semester(self):
        data = {
            'username': 'u_test_registration_view_with_sem',
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
        print("SECOND FORM RESP: ")
        test_user = User.objects.get(username='u_test_registration_view_with_sem')
        self.assertEquals(test_user.studentinfo.semester.semester_number, 2)

    def test_second_form_is_faculty(self):
        
        second_form = FacultyInfoForm()
        resp = self.client.get(
            '/user_management/register/new.html?group=' + str(
                Group.objects.get(name='Faculty').pk),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(second_form.as_ul().encode(), resp.content)

    def test_second_form_faculty_success(self):
        data = {
            'username': 'u_test_registration_view',
            'email': 'dhv2712@gmail.com',
            'password1': 'dhaval27',
            'password2': 'dhaval27',
            'date_of_birth': '22/7/1989',
            'contact_number': '9881585223',
            'group': Group.objects.get(name='Faculty').pk,
            'course': '1'
        }
        resp = self.client.post(
            '/user_management/register/new.html', data=data)
        self.assertTrue('SUCCESS'.encode() in resp.content)

    
