from django import forms
from django.contrib.auth.models import User
from .models.group_info import BasicInfo, StudentInfo
import logging
LOG = logging.getLogger('app')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class BasicInfoForm(forms.ModelForm):
    class Meta:
        model = BasicInfo
        fields = ('date_of_birth', 'contact_number', 'group')


class StudentInfoForm(forms.ModelForm):
    class Meta:
        model = StudentInfo
        fields = ('semester', )
