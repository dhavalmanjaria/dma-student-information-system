from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm


class BasicInfoForm(UserCreationForm):
    date_of_birth = forms.DateField()
    contact_number = forms.CharField(max_length=10)
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(), to_field_name='name')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email',
                  'date_of_birth', 'contact_number', 'group']

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.basicinfo.date_of_birth = self.cleaned_data['date_of_birth']
        user.basicinfo.contact_number = self.cleaned_data['contact_number']
        user.basicinfo.group = Group.objects.get(
            name=self.cleaned_data['group'])

        if commit:
            # Code to add user to group would go here
            user.save()

        return user
