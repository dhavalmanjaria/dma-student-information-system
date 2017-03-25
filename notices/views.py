from django.shortcuts import render
from .models import Notice
from django.views import generic
from .forms import CreateNoticeForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy


class NoticesListView(generic.ListView):    
    paginate_by = 10
    model = Notice

class CreateNotice(generic.edit.CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Notice
    fields = '__all__'
    success_url = reverse_lazy('notices')

    def get_queryset(self):
        return Notice.objects.all().order_by(date)

    class Meta:
        permissions_required = ('can_write_notices', )


class NoticeDetailView(generic.DetailView):
    model = Notice


class UpdateNotice(generic.UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Notice
    fields = '__all__'

    class Meta:
        permissions_required = ('can_write_notices', )
