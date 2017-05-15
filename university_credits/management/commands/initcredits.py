from django.core.management.base import BaseCommand
from curriculum.models import Semester, Subject
from university_credits.models import SubjectCredit, UniversityCredit
from user_management.models.group_info import StudentInfo
import logging
LOG = logging.getLogger('app')


class Command(BaseCommand):
    """
    This command initializes Univeristy Credits for all subjects, for all
    existing students.
    """

    def handle(self, *args, **kwargs):
        for sub in Subject.objects.filter(is_university_subject=True):
            scrd, created = SubjectCredit.objects.get_or_create(
                subject=sub, max_credits=10)
            students = StudentInfo.objects.filter(semester=sub.semester)
            for std in students:
                ucrd, created = UniversityCredit.objects.get_or_create(
                    student=std, credit=scrd)
                if created:
                    ucrd.credit = scrd
                    ucrd.subject = sub
                    ucrd.marks = 0 # by default
                
                    ucrd.save()
           

