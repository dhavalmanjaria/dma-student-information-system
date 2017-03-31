from django.shortcuts import render, redirect
from .models import RoomAssignment, Exam, ExamTimeTable
from django.core.urlresolvers import reverse_lazy
from .forms import RoomAssignmentForm, ExamTimeTableForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, edit
from django.http import JsonResponse
from actions.views import SelectCourseSemester
from curriculum.models import Subject, Course, Semester
from datetime import datetime
import logging

LOG = logging.getLogger('app')


class ExamListView(ListView):
    """
    Shows list of all examinations with the lastest one on first.
    """
    template_name = 'examinations/all-exams.html'
    model = Exam


class UpdateExam(LoginRequiredMixin, PermissionRequiredMixin, edit.UpdateView):
    """
    Update the name and academic year of an exisiting examination. That is,
    only the name and academic year.
    """
    template_name = 'examinations/update-exam.html'
    model = Exam
    fields = '__all__'

    success_url = reverse_lazy('view-exams')

    permission_required = ('user_management.can_write_exam_schedule', )


class CreateExam(LoginRequiredMixin, PermissionRequiredMixin, edit.CreateView):
    template_name = 'examinations/create-exam.html'
    model = Exam
    fields = '__all__'

    success_url = reverse_lazy('view-exams')

    permission_required = ('user_management.can_write_exam_schedule', )        

    def get_context_data(self, **kwargs):
        context = super(CreateExam, self).get_context_data(**kwargs)
        context['current_year'] = datetime.now().year
        return context


class RoomAssignmentList(ListView):
    model = RoomAssignment

    template_name = 'examinations/view-room-assignment.html'

    def get_context_data(self, **kwargs):
        context = super(RoomAssignmentList, self).get_context_data(**kwargs)
        exam_pk = self.kwargs['exam_pk']

        exam = Exam.objects.get(pk=exam_pk)
        context['exam'] = exam
        return context

    def get_queryset(self):
        queryset = super(RoomAssignmentList, self).get_queryset()
        exam_pk = self.request.GET.get('exam_pk')
        exam_pk = self.kwargs['exam_pk']

        exam = Exam.objects.get(pk=exam_pk)
        queryset = queryset.filter(exam=exam).order_by('date')
        return queryset


def _save_room_assignment(ra, form):
    """
    Private, non-public method to save a RoomAssignment if it's a new or
    existing one.
    """
    ra.room_name = form.cleaned_data['room_name']
    ra.start_seat = form.cleaned_data['start_seat']
    ra.end_seat = form.cleaned_data['end_seat']
    ra.date = form.cleaned_data['date']
    ra.subject_name = form.cleaned_data['subject_name']

    LOG.debug(ra)

    ra.save()


def edit_room_assignment(request, exam_pk, date):

    context = {}

    date = datetime.strptime(date, "%d/%m/%Y").date()

    plans = RoomAssignment.objects.filter(date=date)

    exam = Exam.objects.get(pk=exam_pk)

    context['plans'] = plans
    context['plan_date'] = date
    context['exam'] = exam

    if request.method == "POST":
        form = RoomAssignmentForm(request.POST)

        if form.is_valid():

            submit = request.POST.get('submit')

            LOG.debug(submit)
            if submit == "Save":
                pk = request.POST.get('ra_pk')

                ra = RoomAssignment.objects.get(pk=pk)
                _save_room_assignment(ra, form)

            if submit == "Add New":
                ra = RoomAssignment(date=date, exam=exam)
                _save_room_assignment(ra, form)

            if submit == "Delete":
                pk = request.POST.get('ra_pk')
                ra = RoomAssignment.objects.get(pk=pk)
                ra.delete()

        context['form'] = form

    return render(request, 'examinations/edit-room-assignment.html', context)


def select_room_assignment(request, exam_pk):

    context = {}

    exam = Exam.objects.get(pk=exam_pk)

    context['exam'] = exam

    rooms = RoomAssignment.objects.get(exam=exam)
    context['rooms'] = rooms

    if request.method == "POST":
        date = request.POST.get('date')

        return redirect('edit-room-assignment', date=date)

    return render(
        request, 'examinations/select-room-assignment.html', context)


def _save_exam_time_table(tt, form):
    tt.subject = form.cleaned_data['subject']
    tt.date = form.cleaned_data['date']

    tt.save()


def edit_exam_time_table(request, exam_pk, sem_pk):

    context = {}

    exam = Exam.objects.get(pk=exam_pk)

    semester = Semester.objects.get(pk=sem_pk)

    context['exam'] = exam

    context['semester'] = semester

    timetables = ExamTimeTable.objects.filter(
        exam=exam, subject__semester=sem_pk)

    subjects = {}

    for c in Course.objects.all():
        subjects[c] = []
        for sub in Subject.objects.filter(semester__course=c):
            subjects[c].append(sub)

    context['subjects'] = subjects
    context['timetables'] = timetables

    if request.method == "POST":
        form = ExamTimeTableForm(request.POST)
        context['form'] = form

        if form.is_valid():
            submit = request.POST.get('submit')

            if submit == "Save":
                pk = request.POST.get('tt_pk')
                tt = ExamTimeTable.objects.get(pk=pk)
                _save_exam_time_table(tt, form)

            if submit == "Add New":
                pk = request.POST.get('exam')
                exam = Exam.objects.get(pk=pk)
                LOG.debug(exam)
                tt = ExamTimeTable(exam=exam)
                _save_exam_time_table(tt, form)

            if submit == "Delete":
                pk = request.POST.get('tt_pk')
                tt = ExamTimeTable.objects.get(pk=pk)
                tt.delete()

    return render(
        request, 'examinations/edit-exam-time-table.html', context)


class SelectExamTimeTable(SelectCourseSemester):
    """
    This view helps the user select a time table filtered by semester
    """
    def post(self, request, exam_pk):
        exam_pk = request.POST['exam_pk']
        exam = Exam.objects.get(pk=exam_pk)

        semester = super(
            SelectExamTimeTable, self).get_semester_from_post(request)
    
        return redirect('edit-exam-time-table', exam_pk=exam.pk,
                        sem_pk=semester.pk)

    def get(self, request, exam_pk):
        options = super(SelectExamTimeTable, self).get_options(request, all=True)
        context = {}

        if request.is_ajax():
            return JsonResponse(options)

        context['exam'] = Exam.objects.get(pk=exam_pk)



        return render(request, 'examinations/select-exam-time-table.html',
                      context)


class TimeTableList(ListView):
    model = ExamTimeTable

    template_name = 'examinations/view-exam-time-table.html'

    def get_context_data(self, **kwargs):
        context = super(TimeTableList, self).get_context_data(**kwargs)

        exam_pk = self.kwargs['exam_pk']

        exam = Exam.objects.get(pk=exam_pk)
        context['exam'] = exam

        return context

    def get_queryset(self):
        queryset = super(TimeTableList, self).get_queryset()

        exam_pk = self.kwargs['exam_pk']
        sem_pk = self.kwargs['sem_pk']

        semester = Semester.objects.get(pk=sem_pk)

        exam = Exam.objects.get(pk=exam_pk)

        queryset = queryset.filter(
            exam=exam, subject__semester=semester).order_by('date')
        return queryset
