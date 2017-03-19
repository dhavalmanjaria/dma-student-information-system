from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.view_posts, name='view-posts')
]

urlpatterns += [
    url(r'^create-post/(?P<course_pk>[\d]+)$', views.create_post,
        name='create-post')
]

urlpatterns += [
    url(r'^post-comments/(?P<post_pk>[\d]+)$', views.post_comments,
        name='post-comments')
]

urlpatterns += [
    url(r'^edit-post/(?P<post_pk>[\d]+)$', views.edit_post,
        name='edit-post')
]
