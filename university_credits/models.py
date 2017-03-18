from django.db import models
from user_management.models.group_info import StudentInfo
from curriculum.models import Subject


class SubjectCredit(models.Model):
    max_credits = models.IntegerField(default=0)
    subject = models.ForeignKey(Subject)

    class Meta:
        unique_together = ('subject', 'max_credits')

    def __str__(self):
        return str(self.subject.name) + " " + str(self.max_credits)


class UniversityCredit(models.Model):
    student = models.ForeignKey(StudentInfo, null=True)
    credit = models.ForeignKey(SubjectCredit, null=True)
    marks = models.IntegerField(
        help_text='Marks for that student in that subject',
        default=0)

    def __str__(self):
        return str(
            self.student) + " " + str(self.credit)
