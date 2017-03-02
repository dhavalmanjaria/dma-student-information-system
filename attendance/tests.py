from django.test import TestCase
from timetable.models import TimeTable
from user_management.models import User, Group
from user_management.management.commands import initgroups, initcurriculum


class AttendanceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cmd = initgroups.Command()
        cmd.handle()
        cmd = initcurriculum.Command()
        cmd.handle()

        student = Group.objects.get(name='Student')

        std_bca1 = User.objects.create(username='std_bca1')
        std_bca2 = User.objects.create(username='std_bca2')
        std_bca3 = User.objects.create(username='std_bca3')

        StudentInfo.objects.create(user=std_bca1, group=student)
        StudentInfo.objects.create(user=std_bca2, group=student)
        StudentInfo.objects.create(user=std_bca2, group=student)

        TimeTable.objects.create()


    def test_create_attendance(self):
        std_bca1, created = User.objects.get_or_create(username='std_bca1')
        std_bca2, created = User.objects.get_or_create(username='std_bca2')
        std_bca3, created = User.objects.get_or_create(username='std_bca3')

