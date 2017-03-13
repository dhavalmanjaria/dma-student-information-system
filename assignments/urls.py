from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.SelectAssignment.as_view(), name='select-assignment')
]

urlpatterns += [
    url(r'^create-assignment/(?P<subject_pk>[\d]+)', views.create_assignment,
        name='create-assignment')
]#(?P<semester>[\w]+)/(?P<subject>[\w]+)


urlpatterns += [
    url(r'^assignment-list/(?P<subject_pk>[\d]+)',
        views.AssignmentList.as_view(),
        name='assignment-list')
]

urlpatterns += [
    url(r'^assignment-detail/(?P<pk>[\d]+)',
        views.AssignmentDetail.as_view(),
        name='assignment-detail')
]


urlpatterns += [
    url(r'^assignment-update/(?P<pk>[\d]+)',
        views.AssignmentUpdate.as_view(),
        name='assignment-update')
]


