from django.shortcuts import render, redirect
from .models import StudentMetric, Metric
from curriculum.models import Subject, Course, Semester
from user_management.models.group_info import StudentInfo
from django.http import HttpResponse
from .forms import MetricForm
import logging

LOG = logging.getLogger('app')

def edit_metrics(request, pk):
    """
    This view allows faculty to edit metrics for a subject
    """

    context = {}
    form = MetricForm()

    context['form'] = form

    if request.method == "POST":
        form = MetricForm(request.POST)

        new = request.POST.get('new')
        
        if new:
            if form.is_valid():
                subject = Subject.objects.get(pk=pk)

                metric = Metric(subject=subject)
                metric.name = form.cleaned_data['metric_name']
                metric.max_marks = form.cleaned_data['max_marks']

                metric.save()

    subject = Subject.objects.get(pk=pk)
    metrics = Metric.objects.filter(subject=subject)


    context['pk'] = subject.pk
   
    context['metrics'] = metrics
    
    return render(request, 'internal-assessment/edit-metrics.html', context)

def select_course_semester(request):
    context = {}
    course = Course.objects.all()
    context['course'] = course
    semesters = []

    if request.method == "POST":

        if request.is_ajax():
            response = '<option> --- </option>'

            if request.POST.get('course'):
                course = request.POST.get('course')
                semesters = Semester.objects.filter(course__short_name=course)

                for x in semesters:
                    response += "<option>" + str(x) + "</option>"
                LOG.debug(response)
                return HttpResponse(response)

            if request.POST.get('semester'):
                for s in Semester.objects.all():
                    if str(s) == request.POST.get('semester'):
                        semester = s
                subjects = Subject.objects.filter(semester=semester)

                for s in subjects:
                    response += "<option>" + str(s) + "</option>"
                return HttpResponse(response)

        else:
            course = request.POST.get('course')
            semesters = Semester.objects.filter(course__short_name=course)

            semester = [semester for semester in semesters if str(
                semester) == request.POST.get('semester')][0]

            subject = Subject.objects.get(name=request.POST.get('subject'),
                                         semester=semester)

            context['pk'] = subject.pk

            return redirect('student-metric-table', pk=subject.pk)

    return render(request, 'internal-assessment/select-course-semester.html',
                  context)

def student_metric_table(request, pk):
    """
    This view returns the student metrics for a particular subject
    in a particular semester.
    """
    context = {}
    subject = Subject.objects.get(pk=pk)
    context['subject'] = subject

    metrics_for_subject = [mt.name for mt in Metric.objects.filter(
        subject=subject)]

    students = [std for std in StudentInfo.objects.filter(
        semester=subject.semester)]

    metrics = Metric.objects.filter(subject=subject)

    context['metrics'] = metrics

    if len(metrics) == 0:
        return redirect('edit-metrics', pk=pk)
