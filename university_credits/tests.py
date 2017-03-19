from django.test import TestCase
from .models import UniversityCredit, SubjectCredit
from .management.commands import initcredits
from user_management.management.commands import createumuser, initgroups
from curriculum.management.commands import initcurriculum
from curriculum.models import Semester
import logging

LOG = logging.getLogger('app')


class UniversityCreditTestCase(TestCase):
    """
    Note: This testcase does not contain tests to check if credits are created
    when a new student is approved. Those tests are included in
    user_management.tests.test_authentication
    """


    @classmethod
    def setUpTestData(self):
        cmd = initgroups.Command()
        cmd.handle()
        cmd = createumuser.Command()
        cmd.handle()
        cmd = initcurriculum.Command()
        cmd.handle()
        cmd = initcredits.Command()
        cmd.handle()

    def setUp(self):
        global semester
        semester = Semester.objects.get(
            course__short_name="BCA", semester_number=2)

    def test_max_credits(self):
        global semester
        self.client.login(username='um0', password='dhaval27')

        credit = SubjectCredit.objects.filter(
            subject__semester=semester).first()

        LOG.debug(str(credit.pk))
        data = {
            'crd_pk': credit.pk,
            'max_credits': 12
        }

        resp = self.client.post(
            '/actions/university-credits/edit-credits-for-semester/' + str(
                semester.pk), data)

        new_max = SubjectCredit.objects.get(pk=credit.pk).max_credits

        self.assertEqual(new_max, 12)
