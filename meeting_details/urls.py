from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ListMeetings.as_view(), name='all-meetings')
]


urlpatterns += [
    url(r'^edit-meeting/(?P<meeting_pk>[\d]+)$', views.edit_meeting,
        name='edit-meeting')
]

urlpatterns += [
    url(r'^create-meeting/', views.create_meeting,
        name='create-meeting')
]

urlpatterns += [
    url(r'^view-meeting/(?P<meeting_pk>[\d]+)$', views.view_meeting,
        name='view-meeting')
]
