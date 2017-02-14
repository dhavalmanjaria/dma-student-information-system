from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.index, name='index')
]

urlpatterns += [
    url('^register/', views.registration_view, name='register')
]
