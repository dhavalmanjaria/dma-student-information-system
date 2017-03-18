from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
from curriculum.models import Course, Semester, Subject
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
        bba_2, created = Semester.objects.get_or_create(course=bba, semester_number=2)

        bba_4, created = Semester.objects.get_or_create(
            course=bba, semester_number=4)

        bba_6, created = Semester.objects.get_or_create(
            course=bba, semester_number=6)

        # BCA
        bca_2, created = Semester.objects.get_or_create(
            course=bca, semester_number=2)

        bca_4, created = Semester.objects.get_or_create(
            course=bca, semester_number=4)

        bca_6, created = Semester.objects.get_or_create(
            course=bca, semester_number=6)

        # Subject

        # BBA IV
        Subject.objects.get_or_create(
            name='B.Eco', semester=bba_4, is_university_subject=True)

        Subject.objects.get_or_create(
            name='OB-II', semester=bba_4, is_university_subject=True)

        Subject.objects.get_or_create(
            name='B.Envt', semester=bba_4, is_university_subject=True)

        Subject.objects.get_or_create(
            name='Cost & Mgmt a/c', semester=bba_4, is_university_subject=True)

        Subject.objects.get_or_create(
            name='Lead. Skills', semester=bba_4, is_university_subject=False)

        Subject.objects.get_or_create(
            name='Prod. & OP', semester=bba_4, is_university_subject=True)

        Subject.objects.get_or_create(
            name='Advanced Excel', semester=bba_4, is_university_subject=True)

        # BBA II

        Subject.objects.get_or_create(
            name='MM-I', semester=bba_2, is_university_subject=True)

        Subject.objects.get_or_create(
            name='B.Statistics', semester=bba_2, is_university_subject=True)

        Subject.objects.get_or_create(
            name='Comm. Skills', semester=bba_2, is_university_subject=True)

        Subject.objects.get_or_create(
            name='FA', semester=bba_2, is_university_subject=True)

        Subject.objects.get_or_create(
            name='EVS', semester=bba_2, is_university_subject=True)

        Subject.objects.get_or_create(
            name='B. Economics', semester=bba_2, is_university_subject=True)

        # BCA II

        Subject.objects.get_or_create(
            name='OS', semester=bca_2, is_university_subject=True)

        Subject.objects.get_or_create(
            name='SSAD', semester=bca_2, is_university_subject=True)

        Subject.objects.get_or_create(
            name='PPM-I', semester=bca_2, is_university_subject=True)

        Subject.objects.get_or_create(
            name='AWD', semester=bca_2, is_university_subject=True)

        Subject.objects.get_or_create(
            name='Prac. AWD', semester=bca_2, is_university_subject=True)

        # BCA IV

        Subject.objects.get_or_create(
            name='Java', semester=bca_4, is_university_subject=True)

        Subject.objects.get_or_create(
            name='Prac. Java', semester=bca_4, is_university_subject=True)

        Subject.objects.get_or_create(
            name='Oracle', semester=bca_4, is_university_subject=True)

        Subject.objects.get_or_create(
            name='Prac. Oracle', semester=bca_4, is_university_subject=True)

        Subject.objects.get_or_create(
            name='EVS', semester=bca_4, is_university_subject=True)

        Subject.objects.get_or_create(
            name='BA', semester=bca_4, is_university_subject=True)

