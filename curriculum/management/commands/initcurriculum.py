from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
from curriculum.models import Course, Semester
import logging
LOG = logging.getLogger('app')


class Command(BaseCommand):
    """
    This command will initialze the curriculum for the college. In our case,
    we have:
    MBA:
        Sem II
        Sem IV
    BBA:
        Sem II
        Sem IV
        Sem VI
    BCA:
        Sem II
        Sem IV
        Sem VI
    Fact is though, this is in place because sometimes the database needs
    to be wiped because of problems in the migrations.
    """
    help = 'Initialize the curriculum'

    def handle(self, *args, **options):
        mba, created = Course.objects.get_or_create(
            short_name='MBA', long_name='Master of Business Administration')

        bba, created = Course.objects.get_or_create(
            short_name='BBA', long_name='Bachelor of Business Administration')

        bca, created = Course.objects.get_or_create(
            short_name='BCA', long_name='Bachelor of Computer Applications')

        # MBA
        mba_2, created = Semester.objects.get_or_create(
            course=mba, semester_number=2)

        mba_4 = Semester.objects.get_or_create(
            course=mba, semester_number=4)

        # BBA
        bba_2 = Semester.objects.get_or_create(course=bba, semester_number=2)

        bba_4 = Semester.objects.get_or_create(
            course=bba, semester_number=4)

        bba_6 = Semester.objects.get_or_create(
            course=bba, semester_number=6)

        # BCA
        bca_2 = Semester.objects.get_or_create(
            course=bca, semester_number=2)

        bca_4 = Semester.objects.get_or_create(
            course=bca, semester_number=4)

        bca_6 = Semester.objects.get_or_create(
            course=bca, semester_number=6)
