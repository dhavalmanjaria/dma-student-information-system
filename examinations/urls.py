from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^room-assignments/(?P<exam_pk>[\d]+)',
        views.RoomAssignmentList.as_view(),
        name='room-assignments')
]


urlpatterns += [
    url(r'^view-exam-time-table/(?P<exam_pk>[\d]+)',
        views.TimeTableList.as_view(),
        name='view-exam-time-table')
]


urlpatterns += [
    url(r'^$',
        views.ExamListView.as_view(), name='view-exams')
]

urlpatterns += [
    url(r'create-exam/',
        views.CreateExam.as_view(), name='create-exam')
]

urlpatterns += [
    url(r'update-exam/(?P<pk>[\d]+)$',
        views.UpdateExam.as_view(), name='update-exam')
]

urlpatterns += [
    url(r'select-room-assignment/(?P<exam_pk>[\d]+)$',
        views.select_room_assignment,
        name='select-room-assignment')
]

urlpatterns += [
    url(r'edit-room-assignment/(?P<exam_pk>[\d]+)/(?P<date>[\d]{2}/[\d]{2}/[\d]{4})$',
        views.edit_room_assignment, name='edit-room-assignment')
]


urlpatterns += [
    url(r'edit-exam-time-table/(?P<exam_pk>[\d]+)$',
        views.edit_exam_time_table, name='edit-exam-time-table')
]
