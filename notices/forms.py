from django import forms
from notices.models import Notice
from django.urls import reverse_lazy
import logging

LOG = logging.getLogger('app')


class CreateNoticeForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'datepicker'}))

    class Meta:
        model = Notice
        fields = '__all__'
