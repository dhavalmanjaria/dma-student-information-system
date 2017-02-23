from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, BasicInfoForm, StudentInfoForm, FacultyInfoForm
from django.http import HttpResponse
from .models.group_info import BasicInfo
from .models.auth_requests import AuthenticationRequest
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group, User


import logging
LOG = logging.getLogger('app')


def index(request):
    return render(request, 'index.html')


def profile(request):
    username = request.POST['username']
    password = request.POST['password']
    # Must use both authenticate() and login()
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        LOG.debug(request)
        LOG.debug("profile: " + str(user.pk))
        return redirect('user-detail', pk=user.pk)
    else:
        # LOG.debug("invalid username or password")
        return redirect('login')


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


@login_required
def auth_request(request):
    pass
    # For every auth permission that a user has,
    # add those types of requests to the context? thing
    # We see where to go from there
    #
    #
    # But first you need to create a request
