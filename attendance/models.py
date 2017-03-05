from django.db import models
from curriculum.models import Course, Semester, Subject
from user_management.models.group_info import StudentInfo
from timetable.models import TimeTable


class Attendance(models.Model):
    """
    This class represents the attendance for all students across all semesters
    in all lectures.
    """

    # course = models.ForeignKey(Course)
    # semester = models.ForeignKey(Semester)
    date = models.DateField()
    student = models.ForeignKey(StudentInfo)
    lecture = models.ForeignKey(TimeTable)
    is_present = models.BooleanField()

    class Meta:
        unique_together = [['date', 'student', 'lecture'], ]

    def __str__(self):
        return str(self.date) + " " + self.student.user.username +\
            " " + self.lecture.subject.name + " " + str(self.is_present)
