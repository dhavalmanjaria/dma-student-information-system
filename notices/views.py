from django.shortcuts import render
from .models import Notice
from django.views import generic
from .forms import CreateNoticeForm


class NoticesListView(generic.ListView):
    model = Notice

class CreateNotice(generic.edit.CreateView):
    model = Notice
    fields = '__all__'

