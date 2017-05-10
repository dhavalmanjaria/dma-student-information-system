from django import forms
from actions.forms import SelectSemesterForm


class SelectBookStudentForm(SelectSemesterForm):
    book_pk = forms.IntegerField()
