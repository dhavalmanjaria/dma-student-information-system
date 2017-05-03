from django.db import models
from user_management.models.group_info import StudentInfo


class DocumentRequest(models.Model):
    student = models.ForeignKey(StudentInfo)

    DOCUMENT_CHOICES = (
        ('IDC', 'ID Card'),
        ('LBC', 'Library Card'),
        ('RSP', 'Railway Season Pass'),
        ('LBB', 'Library Book'),
        ('BFC', 'Bonafide Certificat'))

    document = models.CharField(choices=DOCUMENT_CHOICES,
                                help_text='Type of the document requested',
                                max_length=3)

