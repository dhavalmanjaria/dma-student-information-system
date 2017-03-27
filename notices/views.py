from django.shortcuts import render
from .models import Notice
from django.views import generic
from .forms import CreateNoticeForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy


class NoticesListView(generic.ListView):    
    paginate_by = 10
    model = Notice

class CreateNotice(LoginRequiredMixin, PermissionRequiredMixin,
                   generic.edit.CreateView):
    model = Notice
    fields = '__all__'
    success_url = reverse_lazy('notices')

    permission_required = ('user_management.can_write_notices', )

    def get_queryset(self):
        return Notice.objects.all().order_by(date)


class NoticeDetailView(generic.DetailView):
    model = Notice


class UpdateNotice(LoginRequiredMixin, PermissionRequiredMixin,
                   generic.edit.UpdateView):
    model = Notice

    fields = '__all__'

    permission_required = ('user_management.can_write_notices', )
