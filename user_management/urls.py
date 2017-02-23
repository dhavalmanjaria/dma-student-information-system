from django.conf.urls import url
from . import views
from django.conf.urls import include
from django.contrib import auth
from django.views.generic.base import RedirectView

urlpatterns = [
#    url('^$', RedirectView.as_view(url='/user_management/accounts/profile/'), name='index')
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
    url(r'^accounts/logout/$', auth.views.logout,
        {'next_page': 'index'})
]

urlpatterns += [
    url('^accounts/', include('django.contrib.auth.urls'))
]

urlpatterns += [
    url('^accounts/profile/', views.profile, name='profile')
]

urlpatterns += [
    url(r'^(?P<pk>\d+)$', views.BasicInfoDetailView.as_view(),
        name='basicinfo-detail')
]
