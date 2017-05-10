from django.db import models
from user_management.models.group_info import StudentInfo


class Book(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    student = models.ForeignKey(StudentInfo)
