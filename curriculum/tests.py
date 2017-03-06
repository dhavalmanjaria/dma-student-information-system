from django.test import TestCase
from .models import Course, Semester
from .management.commands import initcurriculum
from user_management.management.commands import initgroups, createumuser



class CurriculumTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cmd = initgroups.Command()
        cmd.handle()
        cmd = createumuser.Command()
        cmd.handle()
        cmd = initcurriculum.Command()
        cmd.handle()

    # def setUp(self):
    #     bba, create = Course.objects.get_or_create(
    #         short_name='BBA', long_name='Bachelor of Business Administration')
    #     bba.save()

    def test_bba(self):
        bba = Course.objects.get(short_name="BBA")

    def test_create_semester(self):
        bba = Course.objects.get(short_name="BBA")
        bba_2 = Semester.objects.get_or_create(course=bba, semester_number=2)

    def test_courses_created(self):
        bca = Course.objects.get(short_name="BCA")
        bba = Course.objects.get(short_name="BBA")
        mba = Course.objects.get(short_name="MBA")

        self.assertTrue(bca is not None)
        self.assertTrue(bba is not None)
        self.assertTrue(mba is not None)
    