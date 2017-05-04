from django.conf.urls import url
from .views import (
    DocumentRequestListView, grant_document_request, view_my_document_request,
    CreateDocumentRequest)

urlpatterns = [
    url(r'^$', DocumentRequestListView.as_view(), name='all-document-requests')
]

urlpatterns += [
    url(r'^grant/(?P<pk>[\d]+)$', grant_document_request, name='grant-document-request')
]

urlpatterns += [
    url(r'^view-my-document-requests/',
        view_my_document_request,
        name='view-my-document-requests')
]

urlpatterns += [
    url(r'^create-document-request/(?P<pk>[\d]+)$',
        CreateDocumentRequest.as_view(),
        name='create-document-request')
]
