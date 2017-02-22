from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
import datetime
from .models.group_info import BasicInfo, StudentInfo, FacultyInfo
from .models.curriculum import Course, Semester, Subject
import logging
LOG = logging.getLogger('app')


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.password = make_password(self.cleaned_data['password2'])

        if commit:
            user.save()

        return user


class BasicInfoForm(forms.ModelForm):
<<<<<<< HEAD
    student_pk = Group.objects.get(name='Student').pk
    faculty_pk = Group.objects.get(name='Faculty').pk
    subadmin_pk = Group.objects.get(name='SubAdmin').pk
    accounts_pk = Group.objects.get(name='Accounts').pk
    library_pk = Group.objects.get(name='Library').pk
=======
    student_pk = None
    faculty_pk = None
    subadmin_pk = None
    accounts_pk = None
    library_pk = None
    try:
        student_pk = Group.objects.get(name='Student').pk
        faculty_pk = Group.objects.get(name='Faculty').pk
        subadmin_pk = Group.objects.get(name='SubAdmin').pk
        accounts_pk = Group.objects.get(name='Accounts').pk
        library_pk = Group.objects.get(name='Library').pk

    except Exception:
        print("forms.py: Group matching query does not exist, probably")
>>>>>>> 43d358a9a56880351ce932aa6aeb993dfde1e6fe

    group_choices = (
                    ('0', '     '),
                    (student_pk, 'Student'),
                    (faculty_pk, 'Faculty'),
                    (subadmin_pk, 'Sub Admin'),
                    (accounts_pk, 'Accounts'),
                    (library_pk, 'Library'))

    group = forms.ChoiceField(choices=group_choices, initial=0)

    class Meta:
        model = BasicInfo
        fields = ('date_of_birth', 'contact_number', 'group')

    def save(self, commit=True):
        if commit:
            if self.instance is not None:
                self.instance.basicinfo.date_of_birth = self.cleaned_data['date_of_birth']
                self.instance.basicinfo.contact_number = self.cleaned_data['contact_number']
                self.instance.basicinfo.group = Group.objects.get(
                    pk=self.cleaned_data['group'])
                self.instance.save()
            else:
                LOG.debug("BasicInfoForm: instance is None")


class StudentInfoForm(forms.ModelForm):
    class Meta:
        model = StudentInfo
        fields = ('semester', )

    def save(self, commit=True):
        if self.instance is not None:
            s_info = StudentInfo(user=self.instance)
            if commit:
                s_info.semester = self.cleaned_data['semester']
                s_info.save()
                self.instance.studentinfo = s_info

                self.instance.save()

            return s_info


class FacultyInfoForm(forms.ModelForm):

    class Meta:
        model = FacultyInfo
        fields = ('course',)

    def save(self, commit=True):
        if self.instance is not None:
            f_info = FacultyInfo(user=self.instance)
            f_info.course = self.cleaned_data['course']
            f_info.save()
            self.instance.factultyinfo = f_info
            self.instance.save()

        return f_info
