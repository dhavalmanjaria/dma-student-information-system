from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, edit
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin)
from .models import DocumentRequest
from user_management.models.group_info import StudentInfo
import logging

LOG = logging.getLogger('app')


class DocumentRequestListView(LoginRequiredMixin, PermissionRequiredMixin, 
                          ListView):

    model = DocumentRequest

    template_name = 'document-requests/all-document-requests.html'

    # Users with this permission will generally be able to read all
    # document requests
    permission_required = (('user_management.can_read_id_card_req'), )


@login_required
@permission_required('user_management.can_read_id_card_req')
def grant_document_request(request, pk):
    try:
        # If pk does not exist
        document_request = DocumentRequest.objects.get(pk=pk)
        document_request.delete()

    except Exception:
        pass

    return redirect(reverse_lazy('all-document-requests'))


class CreateDocumentRequest(LoginRequiredMixin, PermissionRequiredMixin,
    edit.CreateView):
    
    model = DocumentRequest

    template_name = 'document-requests/create-document-request.html'

    permission_required = (('user_management.can_write_id_card_req'), )

    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(CreateDocumentRequest, self).get_context_data(**kwargs)
        context['student_pk'] = self.kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        form = super(CreateDocumentRequest, self).get_form(self.form_class)

        if form.is_valid():
            dr = DocumentRequest()
            dr.student = form.cleaned_data['student']
            dr.document = form.cleaned_data['document']

            dr.save()

            return redirect(reverse_lazy('view-my-document-requests'))

        return render(request, self.template_name, {'form': form})


@login_required
@permission_required('user_management.can_write_id_card_req')
def view_my_document_request(request):
    context = {}

    student = StudentInfo.objects.filter(user__pk=request.user.pk).first()

    context['student'] = student
    context['document_requests'] = DocumentRequest.objects.filter(
        student=student)


    return render(request, 'document-requests/view-my-document-requests.html',
                  context)
