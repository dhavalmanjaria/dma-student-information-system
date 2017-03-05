from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<pk>[\d]+)/(?P<date>\d\d\d\d-\d\d-\d\d)$',
        views.get_attendance_list, name='attendance-list')
]

urlpatterns += [
    url(r'^save-attendance/(?P<pk>[\d]+)/(?P<date>\d\d\d\d-\d\d-\d\d)$',
        views.save_attendance_list, name='save-attendance-list')
]


urlpatterns += [
    url(r'^select-attendance', views.select, name='select-attendance')
]
