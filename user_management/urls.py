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
    url('^(?P<pk>[-\d]+)/$', views.UserDetailView.as_view(),
        name='user-detail')
]


# urlpatterns += [
#     url(r'^select-subject/', views.SelectSubjectForFaculty.as_view(),
#         name="select-subject")
# ]


urlpatterns += [
    url(r'^set-faculty/(?P<subject_pk>[\d]+)', views.set_faculty,
        name="set-faculty")
]

urlpatterns += [
    url(r'^set-hod/(?P<course_pk>[\d]+)', views.set_hod,
        name="set-hod")
]
