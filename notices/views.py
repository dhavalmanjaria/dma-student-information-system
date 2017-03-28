from django.shortcuts import render
from .models import Notice
from django.views import generic
from .forms import CreateNoticeForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy


class NoticesListView(generic.ListView):    
    paginate_by = 10
    model = Notice
    template_name = 'notices/all-notices.html'

class CreateNotice(LoginRequiredMixin, PermissionRequiredMixin,
                   generic.edit.CreateView):
    model = Notice
    fields = '__all__'
    success_url = reverse_lazy('notices')
    template_name = 'notices/create-notice-html'

    permission_required = ('user_management.can_write_notices', )

    def get_queryset(self):
        return Notice.objects.all().order_by(date)


class NoticeDetailView(generic.DetailView):
    model = Notice
    template_name = 'notices/view-notice.html'


class UpdateNotice(LoginRequiredMixin, PermissionRequiredMixin,
                   generic.edit.UpdateView):
    model = Notice

    fields = '__all__'

    template_name = 'notices/update-notice.html'

    permission_required = ('user_management.can_write_notices', )
