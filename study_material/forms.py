from django import forms
from .models import StudyMaterial


class CreateStudyMaterialForm(forms.ModelForm):

    class Meta:
        model = StudyMaterial
        fields = (('url'), ('title'), ('description'))
