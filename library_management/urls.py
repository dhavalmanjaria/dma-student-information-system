from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.all_books, name='all-books')
]

urlpatterns += [
    url(r'^select-book-student/(?P<book_pk>[\d]+)$',
        views.SelectBookStudent.as_view(), name='select-book-student')
]

urlpatterns += [
    url(r'^set-book-user/(?P<sem_pk>[\d]+)/(?P<book_pk>[\d]+)$',
        views.set_book_user, name='set-book-user')
]
