from django.conf.urls import url
from . import views


urlpatterns = [
    url('^$', views.dashboard, name='dashboard')
]

urlpatterns += [
    url('^requests/', views.auth_requests, name='requests')
]
