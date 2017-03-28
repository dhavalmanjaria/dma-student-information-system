from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.SelectTimeTable.as_view(), name='select-timetable')
]

urlpatterns += [
    url(r'^view-timetable/(?P<pk>[\d]+)', views.view_timetable,
        name='view-timetable')
]

urlpatterns += [
    url(r'^edit-timetable/(?P<pk>[\d]+)', views.edit_timetable,
        name='edit-timetable')
]

urlpatterns += [
    url(r'^edit-times/(?P<pk>[\d]+)', views.edit_times,
        name='edit-times')
]

urlpatterns += [
    url(r'^edit-days/(?P<pk>[\d]+)/(?P<add_rem>[-\w]+)', views.edit_days,
        name='edit-days')
]
