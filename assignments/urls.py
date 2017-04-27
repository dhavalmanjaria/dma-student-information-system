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
    url(r'^all-assignments/(?P<subject_pk>[\d]+)',
        views.AssignmentList.as_view(),
        name='all-assignments')
]

urlpatterns += [
    url(r'^view-assignment/(?P<pk>[\d]+)',
        views.AssignmentDetail.as_view(),
        name='view-assignment')
]


urlpatterns += [
    url(r'^update-assignment/(?P<pk>[\d]+)',
        views.AssignmentUpdate.as_view(),
        name='update-assignment')
]
