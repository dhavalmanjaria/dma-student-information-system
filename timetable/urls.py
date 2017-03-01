from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.select_semester, name='select-semester')
]

urlpatterns += [
    url(r'^view-timetable/(?P<pk>[\d]+)', views.view_timetable,
        name='view-timetable')
]

urlpatterns += [
    url(r'^edit-timetable/(?P<pk>[\d]+)', views.edit_timetable,
        name='edit-timetable')
]