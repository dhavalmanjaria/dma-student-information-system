from django import forms
from curriculum.models import Course, Semester, Subject
from django.core.exceptions import ValidationError


import logging
LOG = logging.getLogger('app')


class SelectSemesterForm(forms.Form):

    course = forms.CharField(required=True)

    semester = forms.CharField(required=True)

    def clean_course(self):
        course = self.cleaned_data['course']
        for c in Course.objects.all():
            if course == c.short_name:
                return c

        raise ValidationError('Invalid course given.')

    def clean_semester(self):
        semester = self.cleaned_data['semester']
        LOG.debug("semester given="+semester)
        for s in Semester.objects.all():
            if semester == str(s):
                return s

        raise ValidationError('Invalid semester given.')


class SelectSubjectForm(SelectSemesterForm):
    subject = forms.CharField()

    def clean_subject(self):
        subject = self.cleaned_data['subject']
        for s in Subject.objects.all():
            if subject == str(s):
                return s

        raise ValidationError('Invalid subject given.')