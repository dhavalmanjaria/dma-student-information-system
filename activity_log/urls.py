from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.SelectActivity.as_view(), name='select-activity')
]

urlpatterns += [
    url(r'^activity-list/(?P<semester_pk>[\d]+)', views.ActivityList.as_view(),
        name='activity-list')
]

urlpatterns += [
    url(r'^create-activity/(?P<semester_pk>[\d]+)',
        views.create_assignment,
        name='create-activity')
]

urlpatterns += [
    url(r'^activity-update/(?P<pk>[\d]+)',
        views.ActivityUpdate.as_view(),
        name='activity-update')
]

urlpatterns += [
    url(r'^activity-detail/(?P<pk>[\d]+)',
        views.ActivityDetail.as_view(),
        name='activity-detail')
]
