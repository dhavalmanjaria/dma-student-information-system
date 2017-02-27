from django.conf.urls import url, include
from . import views
from notices import views as noticesviews

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

