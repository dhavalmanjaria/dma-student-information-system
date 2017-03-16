from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from user_management.models.auth_requests import AuthenticationRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from user_management.models.auth_requests import AuthenticationRequest
from curriculum.models import Course, Semester, Subject
from django.views import View
import logging
import pprint # To remove

LOG = logging.getLogger('app')


@login_required
def dashboard(request):
    # TODO: Filter actions based on permissions
    return render(request, 'dashboard.html')


class SelectCourseSemester(View):
    """
    This is a view that must be inherited by other views so that it gives the
    user the options to select a course and semester and other options based
    on what they're trying to do. The idea is to have a common view to select
    course and semester that adapts to the current action the user is trying
    to perform.
    """
    
    def get_semester_from_post(self, request):
        """
        Gets a semester object from the POST set
        """
        # TODO: Change this to actually use a pk
        semester = request.POST.get('semester')

        semester = [sem for sem in Semester.objects.all() if str(
            sem) == semester][0]

        return semester

    def get_subject_from_post(self, request):
        """
        Gets a subject object from the POST set
        """
        subject_pk = request.POST.get('subject')

        subject = Subject.objects.get(pk=subject_pk)

        return subject

    subjects = []
    def get_options(self, request):
        user = request.user
        subjects = []
        try:
            if user.facultyinfo is not None:  # User is faculty
                subjects = Subject.objects.filter(faculty=user.facultyinfo)

            # I'm trying to avoid checking if the user is assigned to a group
            # explicitly here because if in the future I want to add a different
            # group at the level of FacultyHOD, it would make things easier.
            if user.has_perm('user_management.can_auth_Faculty'):  # User is probably FacHOD
                # Subjects they teach
                subjects = set([s for s in Subject.objects.filter(
                    faculty=user.facultyinfo)])
                # But also all subjects in their course
                courses = [user.facultyinfo.course, ]
                for s in Subject.objects.filter(semester__course_in=course):
                    subjects.add(s)
                LOG.debug(subjects)

        except Exception as ex:
            LOG.debug(str(ex))

        # User is Upper Management level
        if user.has_perm('user_management.can_auth_FacultyHOD'):
            # All subjects for all courses.
            subjects = Subject.objects.all()

        semesters = set(Semester.objects.filter(subject__in=subjects))
        courses = set(Course.objects.filter(semester__in=semesters))

        options = {}

        for c in courses:
            options[c.short_name] = {}
        for sem in semesters:
            course_name = sem.course.short_name
            # options[course_name][(sem.pk, str(sem))] = []
            options[course_name][str(sem)] = []

        for sub in subjects:
            sem = str(sub.semester)
            course_name = sub.semester.course.short_name
            options[course_name][sem].append((sub.pk, sub.name))

        return options

    def get(self, request):
        context = {}

        options = self.get_options(request)

        if request.is_ajax():
                return JsonResponse(options)

        LOG.debug(action)

        pass


#TODO: Move to own app, or at least the user_management app
@login_required
def auth_requests(request):
    """
    This view shows the authentication requests that the current user has the
    permission to grant
    """
    user = request.user
    can_auth_perms = [p.codename for p in user.user_permissions.filter(
        codename__startswith='can_auth_')]

    can_auth_groups = [n.replace('can_auth_', '') for n in can_auth_perms]

    all_requests = set(
        [r for r in AuthenticationRequest.objects.filter(
            group__name__in=can_auth_groups).filter(is_approved=False)])

    context = {}
    context['all_requests'] = all_requests

    return render(request, 'auth_requests.html', context)


@login_required
def grant_request(request):
    """
    This view processes an authentication request and grants the appropriate
    permissions. It does not return a template.
    """
    if request.method == "POST":
        auth_request = AuthenticationRequest.objects.get(pk=request.POST['pk'])
        auth_request.is_approved = True
        auth_request.save()

        user = auth_request.user
        group = auth_request.group

        perms = group.permissions.all()
        user.user_permissions.set(perms)

    return HttpResponse("view complete")
