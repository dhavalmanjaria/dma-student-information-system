from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import render, redirect
from user_management.models.auth_requests import AuthenticationRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from user_management.models.auth_requests import AuthenticationRequest
import logging
LOG = logging.getLogger('app')


@login_required
def dashboard(request):
    # TODO: Filter actions based on permissions
    return render(request, 'dashboard.html')


@login_required
def auth_requests(request):
    user = request.user
    can_auth_perms = [p.codename for p in user.user_permissions.filter(
        codename__startswith='can_auth_')]

    can_auth_groups = [n.replace('can_auth_', '') for n in can_auth_perms]

    all_requests = set(
        [r for r in AuthenticationRequest.objects.filter(
            group__name__in=can_auth_groups)])

    context = {}
    LOG.debug(all_requests)
    context['all_requests'] = all_requests

    return render(request, 'auth_requests.html', context)
