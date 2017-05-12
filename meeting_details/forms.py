from django import forms
from .models import MeetingMinute, Meeting


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        # Time fields added manually
        fields = (('agenda'), ('description'), ('participants'),
                  ('date'))


class MeetingMinuteForm(forms.ModelForm):
    class Meta:
        model = MeetingMinute
        fields = (('text'), )