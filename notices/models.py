from django.db import models
from django.shortcuts import reverse


class Notice(models.Model):
    title = models.CharField(max_length=255, help_text='Title of the Notice')
    PRIORITY_CHOCIES = (('1', 'Very Important'),
                        ('2', 'Important'),
                        ('3', 'General'))

    priority = models.CharField(max_length=1, choices=PRIORITY_CHOCIES)
    date = models.DateField(auto_now=True)
    addressed_to = models.CharField(
        max_length=255, help_text='Everyone that the notice is applies to')
    text = models.TextField()
    other_details = models.TextField()
    signed_by = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('view-notice', args=[self.id, ])  # TODO: Change to view_notice/pk