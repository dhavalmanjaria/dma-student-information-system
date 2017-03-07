from django.shortcuts import render, redirect
from .forms import UserForm, BasicInfoForm, StudentInfoForm, FacultyInfoForm
from django.http import HttpResponse
from .models.group_info import FacultyInfo
from .models.auth_requests import AuthenticationRequest
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from curriculum.models import Course, Subject, Semester
from notices.models import Notice



import logging
LOG = logging.getLogger('app')


def index(request):
    context = {}
    # Here we show the first five records for:
    # Notices
    # TimeTable
    # Activites
    # Assignments
    # Study Materials
    # Exam Schedule
    # Exam Hall Plan

    notices = Notice.objects.all().order_by('date')[:5]

    context['notices'] = notices

    return render(request, 'index.html', context)

@login_required
def profile(request):
    return redirect('user-detail', pk=request.user.pk)


def _getSecondForm(request, user=None):
    if request.method == 'POST':
        group = request.POST.get('group')
        LOG.debug("POST option: " + group)
        try:
            if "Student" == Group.objects.get(id=group).name:
                return StudentInfoForm(
                        request.POST, instance=user)
            if "Faculty" == Group.objects.get(id=group).name:
                return FacultyInfoForm(
                    request.POST, instance=user)
        except Exception:
            print("Group matching query does not exist, probably")
    else:
        group = request.GET.get('group')
        LOG.debug('request is GET and group is ' + group)
        # *Info forms don't have a group property associated with them
        # because BasicInfo already has a group property which stores
        # group info.
        if group == '4':
            return StudentInfoForm()
        if group == '5':
            return FacultyInfoForm()
        if group == '7':
            return AdminInfoForm()


def registration_view(request):
    """
    Registration page
    """
    if request.method == "POST":
        user_form = UserForm(request.POST)
        basic_info_form = BasicInfoForm()

        if user_form.is_valid():
            user = user_form.save()
            LOG.debug('user_form saved')

            basic_info_form = BasicInfoForm(request.POST, instance=user)

            if basic_info_form.is_valid():
                basic_info_form.save()

                second_form = _getSecondForm(request, user=user)

                if second_form.is_valid():
                    second_form.save()
                    LOG.debug('second_form saved')
                    req = AuthenticationRequest.objects.create(
                        user=user,
                        group=user.basicinfo.group)
                    req.save()

                    return redirect("index")
                else:
                    LOG.debug("SECOND FORM ERRORS:" + str(second_form.errors))

            else:
                LOG.debug("BASIC INFO ERRORS:" + str(basic_info_form.errors))

    else:
        user_form = UserForm()
        basic_info_form = BasicInfoForm()

        if request.is_ajax():
            second_form = _getSecondForm(request)
            return HttpResponse(second_form.as_table())  # For JQuery

    return render(request, 'registration/new.html', {
        'user_form': user_form.as_table(),
        'basic_info_form': basic_info_form.as_table()
    })


class UserDetailView(generic.detail.DetailView, LoginRequiredMixin):

    model = User
    template_name = 'user_management/user_detail.html'

    # Append requests to context data
    # Theoretically this should be in it's own view. Added to the GIGANTIC
    # TODO list
    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = context['user']
        can_auth_perms = [p.codename for p in user.user_permissions.filter(
            codename__startswith='can_auth_')]

        can_auth_groups = [n.replace('can_auth_', '') for n in can_auth_perms]

        all_requests = set(
            [r for r in AuthenticationRequest.objects.filter(
                group__name__in=can_auth_groups)])

        LOG.debug(all_requests)
        context['all_requests'] = all_requests
        return context


@login_required
@permission_required('user_management.can_write_subject_faculty')
def select_subject(request):

    context = {}

    courses = Course.objects.all()

    context['courses'] = {}

    for c in courses:
        context['courses'][c.short_name] = []

        semesters = Semester.objects.filter(course=c)
        subjects = []
        for sem in semesters:
            subjects.append([sub for sub in sem.subject_set.all()])
        for s in subjects:
            context['courses'][c.short_name].append(s)


    return render(request, 'user_management/edit_subject_faculty.html',
                  context)

@login_required
@permission_required('user_management.can_write_subject_faculty')
def set_faculty(request, pk):

    context = {}

    faculty = FacultyInfo.objects.all()

    context['faculty'] = faculty

    subject = Subject.objects.get(pk=pk)
    context['subject'] = subject

    current_faculty = subject.faculty
    context['current_faculty'] = current_faculty
    
    if request.method == "POST":
        fac_pk = request.POST.get('fac_pk')

        faculty = FacultyInfo.objects.get(pk=fac_pk)

        subject.faculty = faculty

        subject.save()

        return redirect('select-subject')

    return render(request, 'user_management/set_faculty.html',
                  context)
