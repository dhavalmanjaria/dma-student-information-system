from django.test import TestCase
from timetable.models import TimeTable
from django.contrib.auth.models import User, Group
from user_management.models.group_info import StudentInfo
from user_management.management.commands import initgroups
from curriculum.management.commands import initcurriculum
from attendance.management.commands import createmonthattendance
from curriculum.models import Semester, Subject
from .models import Attendance
# from timetable.tests import TimeTableTest


import logging
LOG = logging.getLogger('app')


class CreateTimeTable:
    """
    Attendance requires a time table to be set up. Therefore this creates a
    time table with public variables for the days, start_times, the semester,
    etc. in __init__() so an appropriate TimeTable is initiated.
    """

    def __init__(self):
        self.start_times = ['0900', '1100', '1300']

        # Get three subjects from BCA II
        self.bca2 = Semester.objects.get(
            course__short_name="BCA", semester_number=2)

        self.os = Subject.objects.get(
            name='OS', semester=self.bca2)
        self.ssad = Subject.objects.get(
            name='SSAD', semester=self.bca2)
        self.awd = Subject.objects.get(
            name='AWD', semester=self.bca2)

        self.subjects = [self.os, self.ssad, self.awd]

        self.days = [1, 2, 3]

        # Delete all old ones
        TimeTable.objects.all().delete()

        # Create 3 day time table
        for sub, t in zip(self.subjects, self.start_times):
            TimeTable.objects.create(day_of_week=1, subject=sub,
                                     start_time=t, semester=self.bca2)

        for sub, t in zip(self.subjects, self.start_times):
            TimeTable.objects.create(day_of_week=2, subject=sub,
                                     start_time=t, semester=self.bca2)

        for sub, t in zip(self.subjects, self.start_times):
            TimeTable.objects.create(day_of_week=3, subject=sub,
                                     start_time=t, semester=self.bca2)


class AttendanceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cmd = initgroups.Command()
        cmd.handle()
        cmd = initcurriculum.Command()
        cmd.handle()

        bca2 = Semester.objects.get(
            course__short_name="BCA", semester_number=2)

        std_bca1, created = User.objects.get_or_create(username='std_bca1')
        std_bca2, created = User.objects.get_or_create(username='std_bca2')
        std_bca3, created = User.objects.get_or_create(username='std_bca3')

        StudentInfo.objects.create(
            user=std_bca1, semester=bca2)
        StudentInfo.objects.create(
            user=std_bca2, semester=bca2)
        StudentInfo.objects.create(
            user=std_bca3, semester=bca2)

        tt_create = CreateTimeTable()

        cmd = createmonthattendance.Command()
        cmd.handle(course='BCA', sem_no=2)


    def test_create_attendance(self):
        pass