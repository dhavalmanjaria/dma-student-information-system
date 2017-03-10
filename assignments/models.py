from django.db import models
from curriculum.models import Subject


class Assignment(models.Model):
    """
    Represents an assignment given to a class (semester)
    """

    title = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject)
    due_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.title + ", " + self.subject.name + ", due: " + str(self.due_date)
