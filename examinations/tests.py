from django.test import TestCase
from user_management.management.commands import initgroups, createumuser
from curriculum.management.commands import initcurriculum
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Permission

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

    def test_edit_room_assignments_access(self):
        url = reverse_lazy(
            'edit-room-assignment',args=1)
        print(url)
        resp = self.client.get(url)

        resp = self.get_wrong_access_response(url)

        self.assertEqual(resp.status_code, 302)
        self.assertTrue('/login' in resp.url)
