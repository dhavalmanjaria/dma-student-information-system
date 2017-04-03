from django.test import TestCase
from user_management.management.commands import initgroups, createumuser
from curriculum.management.commands import initcurriculum
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Permission
from curriculum.models import Semester, Subject

from .models import Exam, ExamTimeTable, RoomAssignment



class ExaminationsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cmd = initgroups.Command()
        cmd.handle()
        cmd = initcurriculum.Command()
        cmd.handle()
        cmd = createumuser.Command()
        cmd.handle()
    
    def setUp(self):
        self.bca2 = Semester.objects.get(
            course__short_name="BCA", semester_number=2)

    def test_exams_are_world_readable(self):
        url = reverse_lazy('all-exams')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

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

        perm = Permission.objects.get(codename='can_write_exam_schedule')
        user.user_permissions.remove(perm)

        resp = self.client.get(
            request_url)

        return resp

    def test_create_exams_access(self):
        url = reverse_lazy('create-exam')
        resp = self.client.get(url)

        resp = self.get_wrong_access_response(url)

        self.assertEqual(resp.status_code, 302)
        self.assertTrue('/login' in resp.url)

    def test_update_exams_access(self):
        url = reverse_lazy('update-exam', args=(1, ))
        resp = self.client.get(url)

        resp = self.get_wrong_access_response(url)

        self.assertEqual(resp.status_code, 302)
        self.assertTrue('/login' in resp.url)

    def test_edit_room_assignments_access(self):
        url = reverse_lazy(
            'edit-room-assignment', args=(1, '01/01/1970'))
        
        resp = self.client.get(url)

        resp = self.get_wrong_access_response(url)

        self.assertEqual(resp.status_code, 302)
        self.assertTrue('/login' in resp.url)

    def test_edit_time_table_access(self):
        url = reverse_lazy(
            'edit-exam-time-table', args=(1,1))
        
        resp = self.client.get(url)

        resp = self.get_wrong_access_response(url)

        self.assertEqual(resp.status_code, 302)
        self.assertTrue('/login' in resp.url)

    def test_create_exam(self):
        self.client.login(username='um0', password='dhaval27')

        post_data = {
            'exam_name': 'test_create_exam',
            'academic_year': 2017
        }

        url = reverse_lazy('create-exam')
        resp = self.client.post(url, post_data)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, reverse_lazy('all-exams'))
        exam = Exam.objects.get(exam_name='test_create_exam')
        self.assertTrue(exam is not None)

    def test_update_exam(self):
        exam = Exam.objects.create(
            exam_name='test_update_exam', academic_year=2017)

        url = reverse_lazy('update-exam', args=(exam.pk, ))
        self.client.login(username='um0', password='dhaval27')

        post_data = {
            'exam_name': 'test_update_exam_change',
            'academic_year': 2017,
            'pk': exam.pk
        }

        self.client.post(url, post_data)

        exam = Exam.objects.get(
            exam_name='test_update_exam_change', academic_year=2017)
        self.assertTrue(exam is not None)

    def test_select_time_table(self):
        exam = Exam.objects.create(
            exam_name='test_select_time_table', academic_year=2017)

        post_data = {
            'course': 'BCA',
            'semester': 'BCA II',
            'exam_pk': exam.pk
        }

        url = reverse_lazy('select-exam-time-table', args=(exam.pk, ))
        tt_url = reverse_lazy(
            'view-exam-time-table', args=(exam.pk, self.bca2.pk))

        self.client.login(username='um0', password='dhaval27')

        resp = self.client.post(url, post_data)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.url, tt_url)

    def test_add_time_table(self):

        self.client.login(username='um0', password='dhaval27')

        exam, created = Exam.objects.get_or_create(
            exam_name='test_add_time_table', academic_year=2017)

        post_data = {
            'date': '02/02/2017',
            'subject': self.bca2.subject_set.first().pk,
            'exam': exam.pk,
            'submit': 'Add New'
        }

        url = reverse_lazy(
            'edit-exam-time-table', args=(exam.pk, self.bca2.pk))

        self.client.post(url, post_data)

        # filter is used here because it's possible that two time tables could
        # be create if tests are not run in a certain order
        exam_tt = ExamTimeTable.objects.filter(exam=exam)

        # Ensure that at least one time table object exists for that exam
        self.assertTrue(len(exam_tt) > 0)

    def test_delete_time_table(self):

        self.client.login(username='um0', password='dhaval27')

        exam, created = Exam.objects.get_or_create(
            exam_name='test_delete_time_table', academic_year=2017)

        exam_tt, created = ExamTimeTable.objects.get_or_create(
            date='2017-02-02',
            subject=self.bca2.subject_set.first(),
            exam=exam)

        post_data = {
            'date': '02/02/2017',
            'subject': self.bca2.subject_set.first().pk,
            'exam': exam.pk,
            'tt_pk': exam_tt.pk,
            'submit': 'Delete'
        }

        url = reverse_lazy(
            'edit-exam-time-table', args=(exam.pk, self.bca2.pk))

        resp = self.client.post(url, post_data)
        # Get old object from database (which shouldn't exist)
        exam_tt = ExamTimeTable.objects.filter(pk=exam_tt.pk)

        self.assertTrue(len(exam_tt) == 0)

    def test_time_table_bad_data(self):
        exam, created = Exam.objects.get_or_create(
            exam_name='test_delete_time_table', academic_year=2017)

        exam_tt, created = ExamTimeTable.objects.get_or_create(
            date='2017-02-02',
            subject=self.bca2.subject_set.first(),
            exam=exam)

        post_data = {
            'date': '02/02-2017',
            'subject': self.bca2.subject_set.first().pk,
            'exam': exam.pk,
            'tt_pk': 9,
            'submit': 'RAKS'
        }

        url = reverse_lazy(
            'edit-exam-time-table', args=(exam.pk, self.bca2.pk))

        resp = self.client.post(url, post_data)
        self.assertEqual(resp.status_code, 302)