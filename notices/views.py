from django.shortcuts import render
from .models import Notice
from django.views import generic
from .forms import CreateNoticeForm
from django.urls import reverse_lazy


class NoticesListView(generic.ListView):
    model = Notice

class CreateNotice(generic.edit.CreateView):
    model = Notice
    fields = '__all__'

    success_url = reverse_lazy('notices')

    def get_queryset(self):
        return Notice.objects.all().order_by(date)


class NoticeDetailView(generic.DetailView):
    model = Notice


class UpdateNotice(generic.UpdateView):
    model = Notice
    fields = '__all__'
