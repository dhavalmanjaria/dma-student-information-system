from django.shortcuts import render, redirect
from actions.views import SelectCourseSemester
from django.http import JsonResponse
from .models import Assignment
from curriculum.models import Semester, Subject
from django.views.generic import DetailView, ListView, UpdateView
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
        subject = super(SelectAssignment, self).get_subject_from_post(request)

        context = {}

        context['subject'] = subject

        return redirect('assignment-list', subject_pk=subject.pk)


    def get(self, request):

        context = {}
        options = super().get_options(request)

        if request.is_ajax():
                return JsonResponse(options)

        return render(request, 'assignments/select-assignments.html',
                      context)


class AssignmentList(ListView):
    model = Assignment

    def get(self, request, subject_pk, *args, **kwargs):
        # subject_pk = self.kwargs['subject']

        self.subject = Subject.objects.get(pk=subject_pk)

        return super(AssignmentList, self).get(request, subject_pk)

    def get_context_data(self, **kwargs):
        context = super(AssignmentList, self).get_context_data(**kwargs)
        context['subject'] = self.subject

        return context

    def get_queryset(self):
        return Assignment.objects.filter(subject=self.subject)


@login_required
@permission_required('user_management.can_write_assignments')
def create_assignment(request, subject_pk):
    """
    Simple view to create assignment. Since we need a subject and we need to
    do some processing, this seems to be simpler than using a CreateView. The
    problem with using a CreateView child class is that it's a little
    complicated to provide the user with a default for date as well as a value
    from the request. This is just simpler.
    """
    subject = Subject.objects.get(pk=subject_pk)
    LOG.debug(subject)

    form = CreateAssignmentForm(initial={'due_date': datetime.now().date()})
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


class AssignmentUpdate(UpdateView, LoginRequiredMixin,
                       PermissionRequiredMixin):

    model = Assignment
    fields = '__all__'

    class Meta:
        permission_required = ('user_management.can_write_assignments', )


class AssignmentDetail(DetailView):
    model = Assignment

    def get_context_data(self, **kwargs):
        context = super(AssignmentDetail, self).get_context_data(**kwargs)

        return context
