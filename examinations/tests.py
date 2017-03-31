from django.test import TestCase
from user_management.management.commands import initgroups, createumuser
from curriculum.management.commands import initcurriculum
from django.urls import reverse_lazy


class ExaminationsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cmd = initgroups.Command()
        cmd.handle()
        cmd = initcurriculum.Command()
        cmd.handle()
        cmd = createumuser.Command()
        cmd.handle()

    def test_exam_time_table_is_world_readable(self):
        url = reverse_lazy('all-exams')
        resp = self.client.get(url)

        print(resp)