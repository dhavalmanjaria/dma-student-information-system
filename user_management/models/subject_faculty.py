from django.db import models
from curriculum.models import Subject
from .group_info import FacultyInfo

class SubjectFaculty(models.Model):
    """
    Model maps a Faculty to the subject that they teach.
    """
    faculty = models.ForeignKey(FacultyInfo)
    subject = models.ForeignKey(Subject)

    class Meta:
        unique_together = ('subject', 'faculty')
