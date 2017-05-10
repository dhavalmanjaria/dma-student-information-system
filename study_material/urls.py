from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^select-study-material/', views.SelectStudyMaterial.as_view(),
        name='select-study-material')
]

urlpatterns += [
    url(r'^all-study-material/(?P<subject_pk>[\d]+)$',
        views.view_study_material, name='all-study-material')
]

urlpatterns += [
    url(r'^create-study-material/(?P<subject_pk>[\d]+)$',
        views.create_study_material, name='create-study-material')
]

urlpatterns += [
    url(r'^edit-study-material/(?P<study_material_pk>[\d]+)$',
        views.edit_study_material, name='edit-study-material')
]