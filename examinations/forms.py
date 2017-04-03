from django import forms
from .models import RoomAssignment, ExamTimeTable
from django.core.exceptions import ValidationError
import logging

LOG = logging.getLogger('app')

class RoomAssignmentForm(forms.ModelForm):

    class Meta:
        model = RoomAssignment
        fields = ('room_name', 'start_seat', 'end_seat', 'date', 'subject_name')

    def clean(self):
        cleaned_data = super(RoomAssignmentForm, self).clean()
        if cleaned_data['start_seat'] > cleaned_data['end_seat']:
            raise ValidationError("Start seat greater than end seat.")
        else:
            return cleaned_data


class ExamTimeTableForm(forms.ModelForm):

    class Meta:
        model = ExamTimeTable
        fields = ('date', 'subject', 'exam')