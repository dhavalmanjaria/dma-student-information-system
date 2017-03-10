from django.shortcuts import render, redirect
from actions.views import SelectCourseSemester
from django.http import JsonResponse
from .models import Assignment
from curriculum.models import Semester, Subject
from django.views.generic import DetailView, ListView, edit
from django.views import View
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import CreateAssignmentForm
from datetime import datetime
import logging

LOG = logging.getLogger('app')


class SelectAssignment(SelectCourseSemester):
    """
    This view represents the select-course-semester page for assignments.
    """

    def post(self, request):
        subject_pk = request.POST.get('subject')

        LOG.debug('post called')

        subject = Subject.objects.get(pk=subject_pk)

        context = {}

        context['subject'] = subject

        assignments = Assignment.objects.filter(subject=subject)

        return redirect('assignment-list', subject_pk=subject_pk)



    def get(self, request):

        context = {}
        options = super().get_options(request)

        if request.is_ajax():
                return JsonResponse(options)

        return render(request, 'assignments/select-assignments.html',
                      context)

    #     if request.POST.get('subject'):
            
    #         subject_pk = request.POST.get('subject')

    #         subject = Subject.objects.get(pk=subject_pk)

    #         context = {}

    #         context['subject'] = subject

    #         redirect('assignment-list', subject_pk=subject_pk)

    #     return render(request, 'assignments/assignment_list.html', context)


class ViewAssignmentsForSubject(View):
    """
    View a list of assignments for a subject.
    """
    

    def post(self, request, subject_pk):
        pass

    def get(self, request, subject_pk):
        context = {}

        subject = Subject.objects.get(pk=subject_pk)

        context['subject'] = subject

        assignments = Assignment.objects.filter(subject=subject)

        context['assignments'] = assignments

        return render(request, 'assignments/assignment_list.html', context)


@login_required
@permission_required('user_management.can_write_assignments')
def create_assignment(request, subject_pk):
    """
    Simple view to create assignment. Since we need a subject and we need to
    do some processing, this seems to be simpler than using a CreateView
    """
    subject = Subject.objects.get(pk=subject_pk)
    LOG.debug(subject)

    form = CreateAssignmentForm()
    context = {}
    context['subject'] = subject
    context['form'] = form

    if request.method == "POST":
        form = CreateAssignmentForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            due_date = form.cleaned_data['due_date']
            subject = subject

            assn = Assignment(subject=subject, description=description,
                              due_date=due_date, title=title)
            assn.save()

            return redirect('assignment-list', subject_pk=subject_pk)



    return render(request, 'assignments/assignment_form.html', context)
