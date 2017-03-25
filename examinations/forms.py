from django import forms
from .models import RoomAssignment, ExamTimeTable


class RoomAssignmentForm(forms.ModelForm):

    class Meta:
        model = RoomAssignment
        fields = ('room_name', 'start_seat', 'end_seat', 'date', 'subject_name')


class ExamTimeTableForm(forms.ModelForm):

    class Meta:
        model = ExamTimeTable
        fields = ('date', 'subject', 'exam')