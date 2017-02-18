from django.test import TestCase
from django.contrib.auth.models import User, Group
from user_management.models.group_info import StudentInfo
from user_management.models.curriculum import Course, Semester
import datetime


class StudentInfoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        global test_user
        group, created = Group.objects.get_or_create(name='Public')
        test_user, created = User.objects.get_or_create(username='test_user')
        test_user.basicinfo.date_of_birth = datetime.datetime.now().date()
        test_user.basicinfo.contact_number = '2929292929'
        test_user.basicinfo.group = group
        test_user.save()

        # Now we create student info explicitly
        s_info = StudentInfo(user=test_user)
        course = Course.objects.create(short_name="BCA")
        semester = Semester.objects.create(course=course, semester_number=2)
        s_info.semester = semester
        s_info.save()

    def test_student_info_exists(self):
        self.assertTrue(test_user.studentinfo is not None)

    def test_semester_number(self):
        self.assertTrue(test_user.studentinfo.semester.semester_number == 2)

    def test_course(self):
        self.assertEquals(test_user.studentinfo.semester.course.short_name, "BCA")
