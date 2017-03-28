from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<pk>[\d]+)/(?P<date>\d\d\d\d-\d\d-\d\d)$',
        views.get_semester_attendance_list, name='attendance-list')
]

urlpatterns += [
    url(r'^view-student-attendance',
        views.get_student_attendance_list,
        name='view-student-attendance')
]


urlpatterns += [
    url(r'^save-attendance/(?P<pk>[\d]+)/(?P<date>\d\d\d\d-\d\d-\d\d)$',
        views.save_attendance_list, name='save-attendance-list')
]


urlpatterns += [
    url(r'^select-attendance',
        views.SelectAttendance.as_view(), name='select-attendance')
]
