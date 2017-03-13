from django import forms
from .models import Activity
from curriculum.models import Semester
import logging

LOG = logging.getLogger('app')


class CreateActivityForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Activity
        fields = ('title', 'date', 'conductor', 'description')
