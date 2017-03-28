from django.shortcuts import render, redirect
from .models import StudentMetric, Metric
from curriculum.models import Subject, Course, Semester
from user_management.models.group_info import StudentInfo, FacultyInfo
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from .forms import MetricForm
from actions.views import SelectCourseSemester
import logging

LOG = logging.getLogger('app')

def _get_auth(request, subject):
    """
    This function checks whether the current user has the permission to edit
    the current metric requested.
    """
    user = request.user
    try:
        if user.has_perm('user_management.can_write_internal_assessment'):
            # Just to make it a little easier to read, I guess.
            if user == subject.semester.course.hod:
                return True
            if user == subject.faculty.user:
                return True
    except Exception as ex:
        LOG.debug(ex)
        
    if user.has_perm('user_management.can_auth_FacultyHOD'):
        return True


@login_required
@permission_required('user_management.can_write_internal_assessment')
def edit_metrics(request, pk):
    """
    This view allows faculty to edit metrics for a subject
    """
    subject = Subject.objects.get(pk=pk)

    context = {}

    user = request.user
    if _get_auth(request, subject):
        context['auth'] = 1

    context = {}
    form = MetricForm()

    students = StudentInfo.objects.filter(semester=subject.semester)
    context['form'] = form

    if request.method == "POST":
        form = MetricForm(request.POST)

        new = request.POST.get('new')
        submit = request.POST.get('submit')

        if new:
            if form.is_valid():
                subject = Subject.objects.get(pk=pk)

                metric = Metric(subject=subject)
                metric.name = form.cleaned_data['metric_name']
                metric.max_marks = form.cleaned_data['max_marks']

                metric.save()

                # Also add metrics for all students
                for std in students:
                    smetric = StudentMetric(student=std)
                    smetric.metric = metric
                    smetric.subject = metric.subject
                    smetric.save()

        if submit == "Save":
            if form.is_valid():
                subject = Subject.objects.get(pk=pk)
                metric_pk = request.POST.get('metric_pk')
                metric = Metric.objects.get(pk=metric_pk)

                metric.name = form.cleaned_data['metric_name']
                metric.max_marks = form.cleaned_data['max_marks']

                metric.save()

                # Also add metrics for all students
                for std in students:
                    smetric = StudentMetric.objects.get(student=std)
                    smetric.metric = metric
                    smetric.subject = metric.subject
                    smetric.save()

        if submit == "Delete":
            if form.is_valid():
                metric_pk = request.POST.get('metric_pk')
                metric = Metric.objects.get(pk=metric_pk)

                metric.delete()

    metrics = Metric.objects.filter(subject=subject)

    context['pk'] = subject.pk
    context['subject'] = subject

    context['metrics'] = metrics

    return render(request, 'internal-assessment/edit-metrics.html', context)


@login_required
@permission_required('user_management.can_write_internal_assessment')
def edit_metrics_for_student(request, std_pk, sub_pk):
    """
    This view allows a user to edit marks for various metrics for a student in
    a particular subject.
    """
    context = {}
    subject = Subject.objects.get(pk=sub_pk)
    student = StudentInfo.objects.get(pk=std_pk)

    student_metrics = StudentMetric.objects.filter(
        student=student, subject=subject)

    context['student_metrics'] = student_metrics

    context['subject'] = subject
    context['student'] = student
    context['auth'] = _get_auth(request, subject)

    if request.method == "POST":
        metric_pk = request.POST.get('metric_pk')
        metric = Metric.objects.get(pk=metric_pk)

        smetric = StudentMetric.objects.get(student=student, subject=subject,
                                            metric=metric)
        smetric.marks = int(request.POST.get('marks'))

        smetric.save()

    return render(
        request, 'internal-assessment/edit-metrics-for-student.html', context)


@login_required
@permission_required('user_management.can_read_internal_assessment')
def student_metric_table(request, subject_pk):
    """
    This view returns the student metrics for a particular subject
    in a particular semester.
    """
    context = {}
    subject = Subject.objects.get(pk=subject_pk)
    context['subject'] = subject

    course = subject.semester.course

    user = request.user
    context['auth'] = _get_auth(request, subject)

    subject = Subject.objects.get(pk=subject_pk)
    context['subject'] = subject

    metrics = Metric.objects.filter(subject=subject)

    context['metrics'] = metrics

    students = StudentInfo.objects.filter(semester=subject.semester)

    student_metrics = {}

    for std in students:
        student_metrics[std] = []
        for m in StudentMetric.objects.filter(subject=subject, student=std):
            student_metrics[std].append(m)

    context['student_metrics'] = student_metrics

    if len(metrics) == 0:
        return redirect('edit-metrics', pk=subject.pk)

    else:
        return render(request, 'internal-assessment/all-internal-assessment.html',
                      context)


def get_student_internal_assessment(request, subject_pk):

    context = {}

    subject = Subject.objects.get(pk=subject_pk)

    student_metrics = StudentMetric.objects.filter(
        subject=subject, student=request.user.studentinfo)

    LOG.debug(student_metrics)

    context['subject'] = subject

    context['student_metrics'] = student_metrics

    return render(request,
                  'internal-assessment/view-student-internal-assessment.html',
                  context)

class SelectInternalAssessment(SelectCourseSemester):
    """
    Select course, semester and subject for internal assessment
    """
    def post(self, request):

        subject = super(SelectInternalAssessment, self).get_subject_from_post(
            request)

        context = {}

        context['subject'] = subject

        # student_metric = StudentMetric.objects.filter(subject=subject)
        
        if StudentInfo.objects.filter(user=request.user).first():
            return redirect('view-student-internal-assessment',
                            subject_pk=subject.pk)

        return redirect(
            'all-internal-assessment', subject_pk=subject.pk)
        

    def get(self, request):

        options = super(SelectInternalAssessment, self).get_options(request)

        LOG.debug(options)

        if request.is_ajax():
            return JsonResponse(options)

        return render(
            request, 'internal-assessment/select-internal-assessment.html')

