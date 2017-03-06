from django.test import TestCase
# from django.contrib.auth.models import User, Group
from user_management.management.commands import initgroups, createumuser
from curriculum.management.commands import initcurriculum
from datetime import datetime
from .models import TimeTable
from curriculum.models import Semester, Subject
from django.contrib.auth import login, authenticate
import logging

LOG = logging.getLogger('app')

class TimeTableTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cmd = initgroups.Command()
        cmd.handle()
        cmd = initcurriculum.Command()
        cmd.handle()
        cmd = createumuser.Command()
        cmd.handle()

    def setUp(self):
        self.start_times = ['0900', '1100', '1300']

        # Get three subjects from BCA II
        self.bca2 = Semester.objects.get(
            course__short_name="BCA", semester_number=2)

        self.os = Subject.objects.get(name='OS', semester=self.bca2)
        self.ssad = Subject.objects.get(name='SSAD', semester=self.bca2)
        self.awd = Subject.objects.get(name='AWD', semester=self.bca2)

        self.subjects = [self.os, self.ssad, self.awd]

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

    def test_monday_time_table(self):
        tt_subs = [tt.subject for tt in TimeTable.objects.filter(
            semester=self.bca2, day_of_week=1)]

        self.assertEqual(tt_subs, self.subjects)

    # Views
    def test_time_table_saved(self):
        post_data = {
            'Monday': ['OS', 'SSAD', 'AWD'],
            'Tuesday': ['OS', 'AWD', 'AWD'],
            'Wednesday': ['OS', 'SSAD', 'AWD'],
            'pk': str(self.bca2.pk)
        }

        self.client.login(username='um0', password='dhaval27')

        resp = self.client.post(
            '/actions/timetable/edit-timetable/' + str(self.bca2.pk),
            data=post_data)

        tt_set = TimeTable.objects.filter(semester=self.bca2, day_of_week=2)

        expected_subs = post_data['Tuesday']

        tt_subs = [tt.subject.name for tt in tt_set]

        self.assertEqual(tt_subs, expected_subs)

    def test_times_created(self):
        post_data = {
            'hours': '9',
            'minutes': '21',
            'a': 'AM',
            'new_lecture': True,
            'submit': 'Add New'
        }

        self.client.login(username='um0', password='dhaval27')

        resp = self.client.post(
            '/actions/timetable/edit-times/' + str(self.bca2.pk),
            data=post_data)

        new_times = [x.start_time for x in TimeTable.objects.filter(
        semester=self.bca2)]

        new_times = sorted(set(new_times), key=int)

        expected_times = ['0900', '0921', '1100', '1300']

        self.assertEqual(new_times, expected_times)

    #TODO: Add test to delete time and day


