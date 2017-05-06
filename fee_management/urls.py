from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.SelectFee.as_view(), name='select-fees')
]

urlpatterns += [
    url(r'^all-fees/(?P<semester_pk>[\d]+)',
        views.FeeCollectionsList.as_view(),
        name='all-fees')
]

urlpatterns += [
    url(r'^add-payment/(?P<std_pk>[\d]+)$', views.add_payment,
        name='add-payment')
]
