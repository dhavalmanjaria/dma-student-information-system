from django.conf.urls import url, include
from . import views
from notices import views as noticesviews
from timetable import views as timetableviews
from internal_assessment import views as iaviews

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

urlpatterns += [
    url(r'^attendance/', include('attendance.urls'))
]

urlpatterns += [
    url(r'^internal-assessment/', include('internal_assessment.urls'))
]

urlpatterns += [
    url(r'select-course-semester', views.select_course_semester,
        name='select-course-semester')
]
