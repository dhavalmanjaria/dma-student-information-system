from django.conf.urls import url
from . import views
from django.conf.urls import include
from django.contrib import auth
from django.views.generic.base import RedirectView

urlpatterns = [
    url('^$', views.index, name='index')
]

urlpatterns += [
    url('^register/', views.registration_view, name='register')
]

urlpatterns += [
    url('^accounts/login/',
        auth.views.login,
        {'template_name': 'registration/login.html'},
        name='login')
]

urlpatterns += [
    url('^accounts/', include('django.contrib.auth.urls'))
]

urlpatterns += [
    url('^accounts/profile/', RedirectView.as_view('/accounts/username'))
]


urlpatterns += [
    url(r'^(?P<username>[-\w]+)/$', views.BasicInfoDetailView.as_view(), name='basicinfo-detail')
]
