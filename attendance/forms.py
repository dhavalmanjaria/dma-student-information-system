from django import forms
from actions.forms import SelectSemesterForm
from datetime import datetime


class SelectAttendanceForm(SelectSemesterForm):
    date = forms.DateField(initial=datetime.now())

# class SelectAttendanceForm(forms.Form):
#     date = forms.DateField()
#     semester = forms.CharField()
