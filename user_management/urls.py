from django.conf.urls import url
from . import views
from django.conf.urls import include
from django.contrib import auth
from django.views.generic.base import RedirectView

urlpatterns = [
    url('^register/', views.registration_view, name='register')
]

# Accounts

urlpatterns += [
    url(r'^accounts/login/',
        auth.views.login,
        {'template_name': 'registration/login.html'},
        name='login')
]

urlpatterns += [
<<<<<<< HEAD
    url(r'^accounts/logout/$', auth.views.logout,
=======
    url(r'^accounts/logout/', auth.views.logout,
>>>>>>> add-doc-requests
        {'next_page': 'index'}, name='logout')
]

urlpatterns += [
    url(r'^accounts/profile/', views.profile, name='profile')
]


urlpatterns += [
    url(r'^accounts/password_reset/$', auth.views.password_reset,
        name='password_reset')
]

urlpatterns += [
    url(r'^accounts/password_reset/done/$',
        auth.views.password_reset_done,
        name='password_reset_done')
]

urlpatterns += [
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
        auth.views.password_reset_confirm, name='password_reset_confirm')
]

urlpatterns += [
    url(r'^reset/done/$', auth.views.password_reset_complete,
        name='password_reset_complete')
]

urlpatterns += [
    url('^(?P<pk>[-\d]+)/$', views.UserDetailView.as_view(),
        name='user-detail')
]

# Set Subject Faculty
urlpatterns += [
    url(r'^set-faculty/(?P<subject_pk>[\d]+)', views.set_faculty,
        name="set-faculty")
]

urlpatterns += [
    url(r'^set-hod/(?P<course_pk>[\d]+)', views.set_hod,
        name="set-hod")
]
