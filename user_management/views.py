from django.shortcuts import render, redirect
from .forms import (
    UserForm, BasicInfoForm, StudentInfoForm, FacultyInfoForm, AdminInfoForm)
from django.http import HttpResponse, JsonResponse
from .models.group_info import FacultyInfo
from .models.auth_requests import AuthenticationRequest
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin)
from django.contrib.auth.models import Group, User, Permission
from django.contrib.auth.forms import SetPasswordForm
from actions.views import SelectCourseSemester
from curriculum.models import Course, Subject
from .management.commands import initgroups
import logging
LOG = logging.getLogger('app')


@login_required
def profile(request):
    """
    Redirect to user's profile page.
    """
    return redirect('user-detail', pk=request.user.pk)


def _getSecondForm(request, user=None):
    """
    Return form for additional information pertaining to a particular group
    info that is inherited from BasicInfo
    """
    if request.method == 'POST':
        group = request.POST.get('group')
        LOG.debug("POST option: " + group)
        try:
            group_name = Group.objects.get(id=group).name
            if "Student" == group_name:
                return StudentInfoForm(
                    request.POST, instance=user)
            if "Faculty" == group_name:
                return FacultyInfoForm(
                    request.POST, instance=user)
            if "SubAdmin" == group_name or "Library" == group_name or "Accounts" == group_name:
                return AdminInfoForm(request.POST)
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
                # basic_info_form.save()

                second_form = _getSecondForm(request, user=user)

                if second_form:
                    if second_form.is_valid():
                        basic_info_form.save()
                        second_form.save()
                        LOG.debug('second_form saved')
                        req = AuthenticationRequest.objects.create(
                            user=user,
                            group=user.basicinfo.group)
                        req.save()
                    else:
                        LOG.debug("SECOND FORM ERRORS:" + str(
                            second_form.errors))

                return redirect("index")

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


class SelectSubjectForFaculty(SelectCourseSemester,
                              LoginRequiredMixin,
                              PermissionRequiredMixin):
    """
    View allows user to select a subject to assign a faculty for.
    """

    class Meta:
        permission_required = 'user_management.can_write_subject_faculty'

    def post(self, request):
        subject = super(
            SelectSubjectForFaculty, self).get_subject_from_post(request)

        return redirect('set-faculty', subject_pk=subject.pk)

    def get(self, request):
        options = super(SelectSubjectForFaculty, self).get_options(request)

        if request.is_ajax():
            return JsonResponse(options)

        return render(request, 'user_management/select-subject-faculty.html')


@login_required
@permission_required('user_management.can_write_subject_faculty')
def set_faculty(request, subject_pk):

    context = {}

    if request.method == "GET":
        context = {}

        faculty = FacultyInfo.objects.all()

        context['faculty'] = faculty
        subject = Subject.objects.get(pk=subject_pk)

        context['subject'] = subject

    if request.method == "POST":

        fac_pk = request.POST.get('fac_pk')
        faculty = FacultyInfo.objects.get(pk=fac_pk)

        subject_pk = request.POST.get('subject_pk')

        subject = Subject.objects.get(pk=subject_pk)

        subject.faculty = faculty

        LOG.debug('saving ' + str(subject.faculty) + ' as faculty for ' + str(
            subject))

        subject.save()

        # That is, reload with get
        return redirect('set-faculty', subject_pk=subject_pk)

    return render(request, 'user_management/set-faculty.html',
                  context)


@login_required
@permission_required('user_management.can_auth_FacultyHOD')
def select_hod_course(request):

    context = {}

    context['courses'] = Course.objects.all()

    return render(request, 'user_management/select-hod-course.html',
                  context)


@login_required
@permission_required('user_management.can_auth_FacultyHOD')
def set_hod(request, course_pk):

    context = {}

    context['course'] = Course.objects.get(pk=course_pk)

    faculty = FacultyInfo.objects.filter(course__pk=course_pk)

    context['faculty'] = faculty

    if request.method == "POST":
        faculty = FacultyInfo.objects.get(pk=request.POST.get('fac_pk'))
        course = Course.objects.get(pk=request.POST.get('course_pk'))

        # TODO: Change course.hod to FacultyInfo rather than User
        # Here we make sure that only HODs have the permissions of HOD

        old_hod = course.hod
        new_hod = faculty.user

        HOD_PERMS = initgroups.PERMISSIONS_BY_ROLE['FacultyHOD']

        for perm in Permission.objects.filter(codename__in=HOD_PERMS):
            if old_hod is not None:
                old_hod.user_permissions.remove(perm)
            new_hod.user_permissions.add(perm)

        #TODO write test for this

        course.hod = new_hod
        course.save()

        return redirect('set-hod', course_pk=course_pk)

    return render(request, 'user_management/set-hod.html',
                  context)


# class PasswordResetView(FormView):
#     """
#     Reset a password for a specific user.
#     """
#     template_name = 'user_management/password_reset_form.html'
#     success_url = 'accounts/password_reset_complete'
#     form_class = SetPasswordForm

#     def post=(self, request, *args, **kwargs):
#         pass