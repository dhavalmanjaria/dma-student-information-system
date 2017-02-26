from django import forms
from noties.models import Notice
import logging

LOG = logging.getLogger('app')


class CreateNoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = '__all__'
