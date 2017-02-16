from django.shortcuts import render
from .forms import UserForm, BasicInfoForm, StudentInfoForm
from django.http import HttpResponse

import logging
LOG = logging.getLogger('app')

def index(request):
    return render(request, 'index.html')


def getSecondForm(request):
    if request.method == 'POST':
        option = request.POST.get('option')
        if option == 3:
            return StudentInfoForm(
                request.POST, instance=request.user.studentinfo)
    else:
        option = request.GET.get('option')
        if option == 3:
            return StudentInfoForm()


def registration_view(request):
    """
    Registration page
    """

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        basic_info_form = BasicInfoForm(
            request.POST, instance=request.user.basicinfo)
        second_form = getSecondForm(request)

        if user_form.is_valid() and basic_info_form.is_valid() and second_form.is_valid():
            user_form.save()
            basic_info_form.save()
            second_form.save()
            return HttpResponse("SUCCESS!!!")
        else:
            return HttpResponse("FAIL")

    else:
        user_form = UserForm()
        basic_info_form = BasicInfoForm()
        
        if request.GET.get('option'):
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
