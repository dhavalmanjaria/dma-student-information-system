from django.shortcuts import render, redirect
from actions.views import SelectCourseSemester
from curriculum.models import Semester
from .models import Activity
from .forms import CreateActivityForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, UpdateView, DetailView, edit
from django.http import JsonResponse
from datetime import datetime


class SelectActivity(SelectCourseSemester):
    """
    View shows the select-course-semester page for Activities
    """

    def post(self, request):
        semester = super(SelectActivity, self).get_semester_from_post(request)

        context = {}

        #TODO: Change this to actually use a pk
        context['semester'] =  semester

        activities = Activity.objects.filter(semester=semester)

        context['activities'] = activities

        return redirect('activity-list', semester_pk=semester.pk)

    def get(self, request):

        context = {}
        options = super().get_options(request)

        if request.is_ajax():
                return JsonResponse(options)

        return render(request, 'activity_log/select-activity.html',
                      context)


class ActivityList(ListView):
    model = Activity

    def get(self, request, semester_pk, *args, **kwargs):

        self.semester = Semester.objects.get(pk=semester_pk)

        return super(ActivityList, self).get(request, semester_pk)

    def get_context_data(self, **kwargs):
        context = super(ActivityList, self).get_context_data(**kwargs)
        context['semester'] = self.semester
        return context

    def get_queryset(self):
        return Activity.objects.filter(semester=self.semester)


@login_required
@permission_required('user_management.can_write_activity_log')
def create_assignment(request, semester_pk):
    """
    Simple view to acreate activity. Similar to the create_assignment view
    """
    semester = Semester.objects.get(pk=semester_pk)

    form = CreateActivityForm(initial={'date': datetime.now().date()})

    context = {}
    context['semester'] = semester
    context['form'] = form

    if request.method == "POST":
        form = CreateActivityForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            conductor = form.cleaned_data['conductor']
            date = form.cleaned_data['date']
            description = form.cleaned_data['description']

            act = Activity(semester=semester,
                           description=description,
                           date=date,
                           title=title,
                           conductor=conductor)
            act.save()

            return redirect('activity-list', semester_pk=semester_pk)

    return render(request, 'activity_log/activity_form.html', context)


class ActivityUpdate(UpdateView, LoginRequiredMixin,
                       PermissionRequiredMixin):

    model = Activity
    fields = '__all__'

    class Meta:
        permission_required = ('user_management.can_write_activity_log', )


class ActivityDetail(DetailView):
    model = Activity

    def get_context_data(self, **kwargs):
        context = super(ActivityDetail, self).get_context_data(**kwargs)

        return context
