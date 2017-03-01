from django.db import models
from curriculum.models import Semester, Subject


class TimeTable(models.Model):
    """
    Represents the time table for all semesters.
    """

    DAY_OF_WEEK_CHOICES = (
                          (1, 'Monday'),
                          (2, 'Tuesday'),
                          (3, 'Wednesday'),
                          (4, 'Thursday'),
                          (5, 'Friday'),
                          (6, 'Saturday'),
                          (7, 'Sunday'))

    day_of_week = models.IntegerField(
        choices=DAY_OF_WEEK_CHOICES,
        help_text='Day of week as per date.isoweekday()')

    subject = models.ForeignKey(Subject)

    start_time = models.CharField(
        max_length=4,
        help_text='Start time in 24h format (easier to work with this way')

    semester = models.ForeignKey(Semester)
