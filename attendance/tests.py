from django.test import TestCase
from timetable.models import TimeTable
from django.contrib.auth.models import User, Group
from user_management.models.group_info import StudentInfo, FacultyInfo
from user_management.management.commands import initgroups
from curriculum.management.commands import initcurriculum
from attendance.management.commands import createmonthattendance
from curriculum.models import Semester, Subject
from .models import Attendance
from datetime import datetime
import calendar
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

        CreateTimeTable()

        cmd = createmonthattendance.Command()
        cmd.handle(course=['BCA', ], sem_no=[6])

    def test_create_attendance(self):
        """
        Ensures one and only one attendance record exists for each student,
        for each lecture, for each day.
        """

        month = datetime.now().month
        year = datetime.now().year
        num_days = calendar.monthrange(year, month)[1]

        dates = [datetime(year, month, x) for x in range(1, num_days + 1)]

        # CreateTimeTable()

        bca6 = Semester.objects.get(
            course__short_name="BCA", semester_number=6)
        days = set([x.day_of_week for x in TimeTable.objects.filter(
            semester=bca6).order_by('day_of_week')])

        for std in StudentInfo.objects.all():
            for dt in dates:
                if dt.isoweekday() in days:
                    lectures = TimeTable.objects.filter(
                        day_of_week=dt.isoweekday(), semester=bca6)
                    # .get() here also ensures that only one attendance object
                    # exists for that date, student, lecture
                    for lect in lectures:
                        self.assertTrue(Attendance.objects.get(
                            date=dt,
                            student=std,
                            lecture=lect) is not None)

    def test_faculty_hod_attendance(self):
        fac_bca_hod, created = User.objects.get_or_create(
            username='fac_bca_hod')
        fac_bca_hod.password = 'dhaval27'
        fac_bca_hod.save()

        FacultyInfo.objects.get_or_create(
            user=fac_bca_hod, course=self.bca2.course)

        self.client.login(username='fac_bca_hod', password='dhaval27')
