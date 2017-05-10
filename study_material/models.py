from django.db import models
from curriculum.models import Subject
from django.contrib.auth.models import User


class StudyMaterial(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    url = models.URLField()
    subject = models.ForeignKey(Subject, null=True)
    date_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
