from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.AttendanceList.as_view(), name='attendance-list')
]
