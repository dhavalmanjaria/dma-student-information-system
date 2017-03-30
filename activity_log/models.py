from django.db import models
from curriculum.models import Semester
from django.urls import reverse


class Activity(models.Model):
    title = models.CharField(max_length=255)
    semester = models.ForeignKey(Semester)
    conductor = models.CharField(max_length=255, help_text='Name of the person'
                                 ' that conducted the activity.')
    description = models.TextField()
    date = models.DateField()

    def get_absolute_url(self):
        return reverse('view-activity', args=[self.id])

    #TODO: add start time and end time, maybe
