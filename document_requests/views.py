from django.shortcuts import render, redirect
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

    return redirect('/document-requests/all-document-requests')


class CreateDocumentRequest(LoginRequiredMixin, PermissionRequiredMixin,
    edit.CreateView):
    
    model = DocumentRequest

    template_name = 'document-requests/create-document-request.html'

    permission_required = (('user_management.can_write_id_card_req'), )

    def post(request, *args, **kwargs):
        return redirect('/document-requests/view-my-document-requests')


@login_required
@permission_required('user_management.can_write_id_card_req')
def view_my_document_request(request):
    context = {}

    student = StudentInfo.objects.filter(user__pk=request.user.pk).first()

    context['document_requests'] = DocumentRequest.objects.filter(
        student=student)

    return render(request, 'document-requests/create-document-request.html',
                  context)
