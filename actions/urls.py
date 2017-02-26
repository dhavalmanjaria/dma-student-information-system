from django.conf.urls import url
from . import views


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