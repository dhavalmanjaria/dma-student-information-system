from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.SelectActivity.as_view(), name='select-activity')
]

urlpatterns += [
    url(r'^all-activities/(?P<semester_pk>[\d]+)', views.ActivityList.as_view(),
        name='all-activities')
]

urlpatterns += [
    url(r'^create-activity/(?P<semester_pk>[\d]+)',
        views.create_activity,
        name='create-activity')
]

urlpatterns += [
    url(r'^update-activity/(?P<pk>[\d]+)',
        views.ActivityUpdate.as_view(),
        name='update-activity')
]

urlpatterns += [
    url(r'^view-activity/(?P<pk>[\d]+)',
        views.ActivityDetail.as_view(),
        name='view-activity')
]
