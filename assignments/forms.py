from django import forms
from .models import Assignment
from curriculum.models import Subject
import logging

LOG = logging.getLogger('app')


class CreateAssignmentForm(forms.ModelForm):

    due_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Assignment
        fields = ('title', 'due_date', 'description',)

