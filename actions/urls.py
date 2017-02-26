from django.conf.urls import url
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
    url('^notices/', noticesviews.NoticesListView.as_view(), name='notices')
]

urlpatterns += [
    url('^create_notice/', noticesviews.CreateNotice.as_view(),
        name='create_notice')
]
