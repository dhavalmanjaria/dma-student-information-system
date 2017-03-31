from django.test import TestCase
from user_management.management.commands import initgroups, createumuser
from curriculum.management.commands import initcurriculum
from .models import TimeTable
from curriculum.models import Semester, Subject
from django.contrib.auth.models import User, Permission
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

    def test_empty_time_table_redirect(self):
        TimeTable.objects.all().delete()
        self.client.login(username='um0', password='dhaval27')

        resp = self.client.get(
            '/actions/timetable/edit-timetable/' + str(self.bca2.pk))

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            resp.url, '/actions/timetable/edit-times/' + str(self.bca2.pk))



    def test_monday_time_table(self):
        tt_subs = [tt.subject for tt in TimeTable.objects.filter(
            semester=self.bca2, day_of_week=1)]

        self.assertEqual(tt_subs, self.subjects)

    # Views
    def test_time_table_saved(self):
        post_data = {
            'Monday': [self.os.pk, self.awd.pk, self.ssad.pk],
            'Tuesday': [self.os.pk, self.awd.pk, self.ssad.pk],
            'Wednesday': [self.os.pk, self.awd.pk, self.ssad.pk],
            'pk': str(self.bca2.pk)
        }

        self.client.login(username='um0', password='dhaval27')

        resp = self.client.post(
            '/actions/timetable/edit-timetable/' + str(self.bca2.pk),
            data=post_data)

        tt_set = TimeTable.objects.filter(semester=self.bca2, day_of_week=2)

        expected_subs = post_data['Tuesday']

        tt_subs = [tt.subject.pk for tt in tt_set]

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

    def test_edit_times_when_empty(self):
        TimeTable.objects.all().delete()
        post_data = {
            'hours': '9',
            'minutes': '21',
            'a': 'AM',
            'new_lecture': True,
            'submit': 'Add New'
        }

        self.client.login(username='um0', password='dhaval27')

        self.client.post(
            '/actions/timetable/edit-times/' + str(self.bca2.pk),
            data=post_data)

        new_times = [x.start_time for x in TimeTable.objects.filter(
            semester=self.bca2)]
        expected_times = ['0921']

        self.assertEqual(new_times, expected_times)        

    def test_time_order_maps_to_subject(self):
        times = [x.start_time for x in TimeTable.objects.filter(
            semester=self.bca2)]

        times = sorted(set(times), key=int)

        tt_set = [tt for tt in TimeTable.objects.filter(
            day_of_week=1, semester=self.bca2).order_by('start_time')]

        subject_times = [tt.start_time for tt in tt_set]

        self.assertEqual(subject_times, times)

    def test_times_added_to_all_rows(self):
        post_data = {
            'hours': '9',
            'minutes': '21',
            'a': 'AM',
            'new_lecture': True,
            'submit': 'Add New'
        }

        self.client.login(username='um0', password='dhaval27')

        # Save time
        resp = self.client.post(
            '/actions/timetable/edit-times/' + str(self.bca2.pk),
            data=post_data)

        new_time = '0921'

        self.days = [1, 2, 3]

        days_with_new_time = 0
        for d in self.days:
            for tt_set in TimeTable.objects.filter(
                    semester=self.bca2, day_of_week=d):
                if tt_set.start_time == '0921':
                    days_with_new_time += 1

        self.assertEqual(days_with_new_time, len(self.days))

    def test_times_saved_to_all_rows(self):
        post_data = {
            'hours': '9',
            'minutes': '21',
            'a': 'AM',
            'lecture_number': 0,
            'submit': 'Save'
        }

        self.client.login(username='um0', password='dhaval27')

        # Save time
        self.client.post(
            '/actions/timetable/edit-times/' + str(self.bca2.pk),
            data=post_data)

        self.days = [1, 2, 3]

        days_with_new_time = 0
        for d in self.days:
            for tt_set in TimeTable.objects.filter(
                    semester=self.bca2, day_of_week=d):
                if tt_set.start_time == '0921':
                    days_with_new_time += 1

        self.assertEqual(days_with_new_time, len(self.days))

    def test_all_timetables_are_world_readable(self):
        for sem in Semester.objects.all():
            resp = self.client.get(
                '/actions/timetable/view-timetable/' + str(sem.pk))
            self.assertEqual(resp.status_code, 200)

    def test_time_maps_to_subject(self):
        semester = Semester.objects.get(pk=6)
        tt = TimeTable.objects.filter(day_of_week=1, semester=semester)

        monday = tt.get(start_time='0900')

        self.assertEqual(monday.subject, self.os)

    def test_add_new_day(self):
        """
        Ensures that a day is added and has three lectures, one for each start
        time
        """
        post_data = {
            'new_day': 4,
            'add_rem': 'Add'
        }

        self.client.login(username='um0', password='dhaval27')

        self.client.post('/actions/timetable/edit-days/6', post_data)

        tt = TimeTable.objects.filter(day_of_week=4, semester=self.bca2)

        self.assertEqual(len(tt), len(self.start_times))

    def test_add_new_day_when_empty(self):
        TimeTable.objects.all().delete()
        self.test_edit_times_when_empty()
        post_data = {
            'new_day': 1,
            'add_rem': 'Add'
        }

        self.client.login(username='um0', password='dhaval27')

        self.client.post('/actions/timetable/edit-days/6', post_data)

        tt = TimeTable.objects.filter(
            day_of_week=1, semester=self.bca2)

        self.assertEqual(len(tt), 1)  # One for one lecture.

    def test_rem_new_day(self):
        post_data = {
            'new_day': 1,
            'add_rem': 'Delete'
        }
        semester = Semester.objects.get(pk=6)

        self.client.login(username='um0', password='dhaval27')

        self.client.post('/actions/timetable/edit-days/6', post_data)

        tt = TimeTable.objects.filter(day_of_week=1, semester=semester)

        self.assertEqual(len(tt), 0)

    def test_times_removed_from_all_days(self):
        post_data = {
            'hours': '9',
            'minutes': '21',
            'a': 'AM',
            'lecture_number': 0,
            'submit': 'Delete'
        }

        old_time = '0921'

        self.client.login(username='um0', password='dhaval27')

        # Save time
        self.client.post(
            '/actions/timetable/edit-times/' + str(self.bca2.pk),
            data=post_data)

        tt = TimeTable.objects.filter(start_time=old_time, semester=self.bca2)

        self.assertEqual(len(tt), 0)

    def get_wrong_access_response(self, request_url):
        """
        Get a Response object for a user that doesn't have a permission
        trying to edit something.
        """

        # Create a user that has some permissions but not can_write_timetable
        user, created = User.objects.get_or_create(username='test_access_user')

        user.password = 'dhaval27'
        user.save()

        um0 = User.objects.get(username='um0')

        user.user_permissions.set(um0.user_permissions.all())

        tt_perm = Permission.objects.get(codename='can_write_time_table')
        user.user_permissions.remove(tt_perm)

        resp = self.client.get(
            request_url)

        return resp

    def test_access_edit_times(self):
        resp = self.get_wrong_access_response(
            '/actions/timetable/edit-times/' + str(self.bca2.pk))

        self.assertTrue(resp.status_code == 302)
        self.assertTrue('/login' in resp.url)

    def test_access_edit_days(self):

        resp = self.get_wrong_access_response(
            request_url='/actions/timetable/edit-days/' + str(self.bca2.pk))

        self.assertTrue(resp.status_code == 302)
        self.assertTrue('/login' in resp.url)

    def test_access_edit_time_table(self):

        resp = self.get_wrong_access_response(
            request_url='/actions/timetable/edit-timetable/' + str(self.bca2.pk))

        self.assertTrue(resp.status_code == 302)
        self.assertTrue('/login' in resp.url)

    def test_subjects_only_exist_for_times(self):
        for sub in self.subjects:
            tt = TimeTable.objects.filter(semester=self.bca2, subject=sub)
            self.assertEqual(len(tt), len(self.start_times))