from django.conf.urls import url, include
from . import views
from notices import views as noticesviews
from timetable import views as timetableviews
from internal_assessment import views as iaviews
import user_management

urlpatterns = [
    url('^$', views.dashboard, name='dashboard')
]


urlpatterns += [
    url(r'^requests/', views.auth_requests, name='requests')
]

urlpatterns += [
    url(r'^select-option/(?P<action>[-\w]+)',
        views.SelectCourseSemester.as_view(),
        name='select-option')
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
    url(r'^assignments/', include('assignments.urls'))
]

urlpatterns += [
    url(r'^activity-log/', include('activity_log.urls'))
]

urlpatterns += [
    url(r'^select-subject/',
        user_management.views.SelectSubjectForFaculty.as_view(),
        name="select-subject")
]

urlpatterns += [
    url(r'^select-hod-course/',
        user_management.views.select_hod_course,
        name="select-hod-course")
]

urlpatterns += [
    url(r'^university-credits/', include('university_credits.urls'))
]
