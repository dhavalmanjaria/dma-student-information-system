from django.conf.urls import url, include
from . import views
<<<<<<< HEAD
from notices import views as noticesviews
=======
from timetable import views as timetableviews

>>>>>>> add-time-table

urlpatterns = [
    url('^$', views.dashboard, name='dashboard')
]

urlpatterns += [
    url(r'^requests/', views.auth_requests, name='requests')
]

urlpatterns += [
    url(r'^grant_request/$', views.grant_request,
        name='grant_request')
]

urlpatterns += [
    url('^notices/', include('notices.urls'))
]

urlpatterns += [
    url(r'^timetable/', include('timetable.urls'))
]
