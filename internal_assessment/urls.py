from django.conf.urls import url
from . import views


urlpatterns = [
   url('^$', views.select_course_semester, name='internal-assessment')
]

urlpatterns += [
    url(r'^student-metric-table/(?P<pk>[\d]+)', views.student_metric_table,
        name='student-metric-table')
]

urlpatterns += [
    url(r'^edit-metrics/(?P<pk>[\d]+)', views.edit_metrics,
        name='edit-metrics')
]
