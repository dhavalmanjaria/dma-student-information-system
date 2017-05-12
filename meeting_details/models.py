from django.db import models


class Meeting(models.Model):
    agenda = models.CharField(max_length=200,
                              help_text='The title or purpose of the meeting')
    description = models.CharField(max_length=200)
    participants = models.CharField(max_length=1000)

    date = models.DateField(auto_now=False, null=True)
    time = models.TimeField(null=True)

    class Meta:
        ordering = ('-date', '-time')


class MeetingMinute(models.Model):
    """
    Represents a line item that makes up the minutes of a meeting
    """
    text = models.CharField(max_length=200)
    meeting = models.ForeignKey(Meeting, null=True)
    time = models.TimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('time', )
