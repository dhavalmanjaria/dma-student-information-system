from django.db import models
from datetime import datetime
from curriculum.models import Subject


class Exam(models.Model):
    exam_name = models.CharField(
        max_length=200, help_text='Name of the examination')
    academic_year = models.PositiveIntegerField(
        help_text='Year that the academic year started in.',
        default=datetime.now().year)

    class Meta:
        unique_together = ('exam_name', 'academic_year')

    def __str__(self):
        return "%s %s - '%s" % (self.exam_name,
                                str(self.academic_year),
                                str(self.academic_year + 1)[2:])


class ExamTimeTable(models.Model):
    exam = models.ForeignKey(Exam, null=True)
    subject = models.ForeignKey(Subject)
    date = models.DateField(null=True)

    def __str__(self):
        return "%s %s %s" % (self.exam.exam_name,
                             self.subject,
                             str(self.date))


class RoomAssignment(models.Model):

    room_name = models.CharField(
        max_length=200, help_text='Name or number of the room')
    start_seat = models.IntegerField()
    end_seat = models.IntegerField()
    exam = models.ForeignKey(Exam, null=True)
    subject_name = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(null=True)

    def __str__(self):
        return "%s %s - %s on %s" % (self.room_name,
                                     str(self.start_seat),
                                     str(self.end_seat),
                                     str(self.date))
