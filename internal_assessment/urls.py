from django.conf.urls import url
from . import views


urlpatterns = [
   url('^$', views.SelectInternalAssessment.as_view(), name='select-internal-assessment')
]

urlpatterns += [
    url(r'^all-internal-assessment/(?P<subject_pk>[\d]+)', views.student_metric_table,
        name='all-internal-assessment')
]

urlpatterns += [
    url(r'^student-internal-assessment/(?P<subject_pk>[\d]+)',
        views.get_student_internal_assessment,
        name='view-student-internal-assessment')
]

urlpatterns += [
    url(r'^edit-metrics/(?P<pk>[\d]+)', views.edit_metrics,
        name='edit-metrics')
]

urlpatterns += [
    url(r'edit-metrics-for-student/(?P<std_pk>[\d]+)/(?P<sub_pk>[\d]+)',
        views.edit_metrics_for_student,
        name='edit-metrics-for-student')
]
