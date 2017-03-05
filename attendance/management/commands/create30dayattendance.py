from django.core.management.base import BaseCommand
from attendance.models import Attendance
from timetable.models import TimeTable
import logging

LOG = logging.getLogger('app')

class Command(BaseCommand):
    """
    This command creates one month of attendance for the current month.
    """

