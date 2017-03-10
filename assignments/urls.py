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
        views.ViewAssignmentsForSubject.as_view(),
        name='assignment-list')
]