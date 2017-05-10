from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin)
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import (
    login_required, permission_required)
from .models import StudyMaterial
from curriculum.models import Subject
from .forms import CreateStudyMaterialForm
from actions.views import SelectCourseSemester
from actions.forms import SelectSubjectForm


class SelectStudyMaterial(SelectCourseSemester):
    form = SelectSubjectForm
    redirect_to = 'all-study-material'
    select_template = 'study-material/select-study-material.html'
    context = {}

    def post(self, request):
        subject = super(SelectStudyMaterial, self).get_subject_from_post(
            request)

        context = {}

        context['subject'] = subject

        return redirect('all-study-material', subject_pk=subject.pk)


def view_study_material(request, subject_pk):
    context = {}

    subject = Subject.objects.get(pk=subject_pk)

    study_material = StudyMaterial.objects.filter(subject=subject)

    context['subject'] = subject
    context['study_material'] = study_material

    return render(request, 'study-material/all-study-material.html', context)


# TODO: Fix typo, replace 'study_materials' with singular
@login_required
@permission_required('user_management.can_write_study_materials')
def create_study_material(request, subject_pk):
    context = {}

    subject = Subject.objects.get(pk=subject_pk)

    form = CreateStudyMaterialForm()

    context['form'] = form
    context['subject'] = subject

    if request.method == "POST":
        form = CreateStudyMaterialForm(request.POST)

        if form.is_valid():
            study_material = StudyMaterial()
            study_material.title = form.cleaned_data['title']
            study_material.description = form.cleaned_data['description']
            study_material.url = form.cleaned_data['url']
            study_material.user = request.user
            study_material.subject = subject

            study_material.save()

        return redirect('all-study-material', subject_pk=subject.pk)

    return render(request, 'study-material/create-study-material.html',
                  context)


@login_required
@permission_required('user_management.can_write_study_materials')
def edit_study_material(request, study_material_pk):
    context = {}

    study_material = StudyMaterial.objects.get(pk=study_material_pk)

    form = CreateStudyMaterialForm(
        initial={'title': study_material.title,
                 'description': study_material.description,
                 'url': study_material.url})

    if request.user != study_material.user:
        raise PermissionDenied

    if request.method == "POST":
        form = CreateStudyMaterialForm(request.POST)
        if form.is_valid():
            study_material_pk = request.POST.get('study_material_pk')
            study_material = StudyMaterial.objects.get(pk=study_material_pk)

            study_material.title = form.cleaned_data['title']
            study_material.description = form.cleaned_data['description']
            study_material.url = form.cleaned_data['url']

            study_material.save()

            return redirect('all-study-material',
                            subject_pk=study_material.subject.pk)

    context['form'] = form
    context['study_material'] = study_material

    return render(request, 'study-material/update-study-material.html',
                  context)
