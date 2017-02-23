from django.test import TestCase
from .models import Course, Semester


class CurriculumTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        bba = Course.objects.create(
            short_name='BBA', long_name='Bachelor of Business Administration')
        bba.save()


    def test_bba(self):
        bba = Course.objects.get(short_name="BBA")

    def test_create_semester(self):
        bba = Course.objects.get(short_name="BBA")
        bba_2 = Semester.objects.get_or_create(course=bba, semester_number=2)