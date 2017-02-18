from django.shortcuts import render
from .forms import UserForm, BasicInfoForm, StudentInfoForm, FacultyInfoForm
from django.http import HttpResponse
from .models.group_info import BasicInfo
from django.views.generic.detail import DetailView

import logging
LOG = logging.getLogger('app')


def index(request):
    return render(request, 'index.html')


def getSecondForm(request, user=None):
    if request.method == 'POST':
        group = request.POST.get('group')
        LOG.debug("POST option: " + group)
        if group == '4':
            return StudentInfoForm(
                request.POST, instance=user)
        if group == '5':
            return FacultyInfoForm(
                request.POST, instance=user)
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

        if user_form.is_valid():
            user = user_form.save()
            LOG.debug('user_form saved')

            basic_info_form = BasicInfoForm(
                request.POST, instance=user)

            if basic_info_form.is_valid():
                basic_info_form.save()

                second_form = getSecondForm(request, user=user)

                if second_form.is_valid():
                    second_form.save()
                    LOG.debug('second_form saved')

                    return HttpResponse("SUCCESS!!!")
                else:
                    LOG.debug("SECOND FORM ERRORS:" + str(second_form.errors))

            else:
                LOG.debug("BASIC INFO ERRORS:" + str(basic_info_form.errors))

    else:
        user_form = UserForm()
        basic_info_form = BasicInfoForm()

        if request.is_ajax():
            second_form = getSecondForm(request)
            return HttpResponse(second_form.as_table())  # For JQuery

    return render(request, 'registration/new.html', {
        'user_form': user_form.as_table(),
        'basic_info_form': basic_info_form.as_table()
    })

    # if request.method == 'POST':
    #     basic_info_form = BasicInfoForm(request.POST)
    #     std_form = StudentInfoForm(request.POST)

    #     LOG.debug(basic_info_form)
    #     LOG.debug(std_form)

    #     if basic_info_form.is_valid() and std_form.is_valid():
    #         basic_info_form.save()
    #         std_form.save()

    # else:
    #     basic_info_form = BasicInfoForm()
    #     if request.GET.get('option'):
    #         std_form = StudentInfoForm()
    #         return HttpResponse(std_form.as_table())

    # return render(request, 'registration/new.html',
    #               {'basic_info_form': basic_info_form.as_table()})


class BasicInfoDetailView(DetailView):
    model = BasicInfo

