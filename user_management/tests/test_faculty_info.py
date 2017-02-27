from django.test import TestCase
from django.contrib.auth.models import User, Group
from user_management.models.group_info import FacultyInfo
from curriculum.models import Course
import datetime


class FacultyInfoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        global test_user
        group, created = Group.objects.get_or_create(name='Public')
        test_user, created = User.objects.get_or_create(username='u_test_faculty_info')
        test_user.basicinfo.date_of_birth = datetime.datetime.now().date()
        test_user.basicinfo.contact_number = '2929292929'
        test_user.basicinfo.group = group
        test_user.save()

        # Now we create student info explicitly
        f_info = FacultyInfo(user=test_user)
        course = Course.objects.create(short_name="BCA")
        f_info.course = course
        f_info.save()

    def test_faculty_info_exists(self):
        self.assertTrue(test_user.facultyinfo is not None)

    def test_course(self):
        self.assertTrue(test_user.facultyinfo.course.short_name == "BCA")
