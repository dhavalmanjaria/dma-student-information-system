from django.shortcuts import render
from .forms import BasicInfoForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def registration_view(request):
    """
    Registration page
    """
    if request.method == 'POST':
        form = BasicInfoForm(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('index'))

    else:
        form = BasicInfoForm()

    return HttpResponse(form.as_p())
