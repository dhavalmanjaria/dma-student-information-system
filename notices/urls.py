from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.NoticesListView.as_view(), name='notices')
]

urlpatterns += [
    url('^create_notice/', views.CreateNotice.as_view(),
        name='create-notice')
]

urlpatterns += [
    url(r'^view_notice/(?P<pk>\d+)',
        views.NoticeDetailView.as_view(), name='view-notice')
]

urlpatterns += [
    url(r'^update_notice/(?P<pk>\d+)', views.UpdateNotice.as_view(),
        name='update-notice')
]
