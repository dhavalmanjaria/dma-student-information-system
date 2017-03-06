from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import render, redirect
from django.http import HttpResponse
from user_management.models.auth_requests import AuthenticationRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from user_management.models.auth_requests import AuthenticationRequest
from curriculum.models import Course, Semester
import logging
LOG = logging.getLogger('app')


@login_required
def dashboard(request):
    # TODO: Filter actions based on permissions
    return render(request, 'dashboard.html')


def select_course_semester(request):
    """
    This view gives the user to select a course and semester and
    other options based on what they're trying to do. The idea is to have a
    common view to select course and semester that adapts to the current
    action the user is trying to perform
    """
    context = {}
    semester = Semester.objects.all()
    course = Course.objects.all()
    context['course'] = course

    #TODO: Use a form, maybe
    if request.method == "POST":

        course = request.POST.get('course')
        semesters = Semester.objects.filter(course__short_name=course)

        if request.is_ajax():
            response = ''
            for x in semesters:
                response += "<option>" + str(x) + "</option>"
            LOG.debug(response)
            return HttpResponse(response)

        else:
            semester = [semester for semester in semesters if str(
                semester) == request.POST.get('semester')][0]

            context['pk'] = semester.pk
            
    return render(request, 'actions/select_course_semester.html', context)

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
