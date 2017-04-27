from django.core.management.base import BaseCommand
from attendance.models import Attendance
from timetable.models import TimeTable
from curriculum.models import Semester, Subject
from user_management.models.group_info import StudentInfo
from datetime import datetime, timedelta
import calendar
import logging

LOG = logging.getLogger('app')


class Command(BaseCommand):
    """
    This command creates one month of attendance for the current month.
    """

    def _get_weekday(d):
        weekdays = {
            1: 'Monday',
            2: 'Tuesday',
            3: 'Wednesday',
            4: 'Thursday',
            5: 'Friday',
            6: 'Saturday'
        }

        return weekdays[d]

    def add_arguments(self, parser):
        parser.add_argument('course', type=str, nargs='+')
        parser.add_argument('sem_no', type=int, nargs='+')

    def handle(self, *args, **options):
        LOG.debug(options)

        course_name = options['course'][0]
        sem_no = int(options['sem_no'][0])

        LOG.debug(options)

        LOG.debug(course_name)

        semester = Semester.objects.get(
            course__short_name=course_name, semester_number=sem_no)
        
        month = datetime.now().month
        year = datetime.now().year
        num_days = calendar.monthrange(year, month)[1]

        # LOG.debug(num_days)

        dates = [datetime(year, month, x) for x in range(1, num_days + 1)]

        days = set([x.day_of_week for x in TimeTable.objects.filter(
            semester=semester).order_by('day_of_week')])

        students = [sinfo for sinfo in StudentInfo.objects.filter(
            semester=semester)]

        tomorrow = datetime.today().date() + timedelta(days=1)

        for std in students:  # For each student
            for dt in dates:  # on each day
                # date is a working day and is in the future
                if dt.isoweekday() in days and tomorrow > dt.date():
                    lectures = TimeTable.objects.filter(
                        day_of_week=dt.isoweekday(), semester=semester)
                    for lect in lectures:  # for each lecture on that day
                        # create an attendance record
                        att, created = Attendance.objects.get_or_create(
                            date=dt, student=std, lecture=lect)
                        if created:
                            att.is_present = False
                            att.save()
