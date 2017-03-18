from django.conf.urls import url, include
from . import views


urlpatterns = [
    url('^$', views.SelectCredits.as_view(),
        name='select-credits')
]

urlpatterns += [
    url(r'^credits-list/(?P<semester_pk>[\d]+)$',
        views.get_credit_list,
        name='credits-list')
]


urlpatterns += [
    url(r'^edit-credits-for-semester/(?P<semester_pk>[\d]+)$',
        views.edit_credits_for_semester,
        name='edit-credits-for-semester')
]

urlpatterns += [
    url(r'^edit-credits-for-student/(?P<std_pk>[\d]+)$',
        views.edit_credits_for_student,
        name='edit-credits-for-student')
]
