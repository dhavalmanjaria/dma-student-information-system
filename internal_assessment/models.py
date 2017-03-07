from django.db import models
from curriculum.models import Subject
from user_management.models.group_info import StudentInfo


class Metric(models.Model):
    """
    Represents a metric that can be assigned in a subject.
    Theoretically these are mutli-valued attributes of the subject
    entity
    """
    name = models.CharField(max_length=20)
    max_marks = models.IntegerField(help_text='Maximum marks that can be '
                                              'allotted in a metric')
    
    subject = models.ForeignKey(Subject)

    class Meta:
        # Each record that belongs to a metric of a subject, will have
        # the same maximum marks. Theoretically
        unique_together = ('subject', 'name', 'max_marks')
        ordering = ('name', )

    def __str__(self):
        return self.subject.name + ": " + self.name

    #TODO: add absolute url for metric detail


class StudentMetric(models.Model):
    """
    This will be the final table that we will use. Each student has metrics
    for each subject. All students have the same metrics for each subject
    """

    student = models.ForeignKey(StudentInfo)
    subject = models.ForeignKey(Subject)
    metric = models.ForeignKey(Metric)
    marks = models.IntegerField(help_text='Marks for that student in that'
                                          ' metric', default=0)

    class Meta:
        unique_together = ('student', 'subject', 'metric')
        ordering = ('metric', )

    def __str__(self):
        return ', '.join([str(self.student), self.subject.name,
                          self.metric.name])
