from django.shortcuts import render, redirect
from .models import RoomAssignment, Exam, ExamTimeTable
from django.core.urlresolvers import reverse_lazy
from .forms import RoomAssignmentForm, ExamTimeTableForm
from django.views.generic import ListView, edit
from curriculum.models import Subject, Course
from datetime import datetime
import logging

LOG = logging.getLogger('app')


class ExamListView(ListView):
    template_name = 'examinations/view-exams.html'
    model = Exam


class UpdateExam(edit.UpdateView):
    template_name = 'examinations/update-exam.html'
    model = Exam
    fields = '__all__'

    success_url = reverse_lazy('view-exams')


class CreateExam(edit.CreateView):
    template_name = 'examinations/create-exam.html'
    model = Exam
    fields = '__all__'

    success_url = reverse_lazy('view-exams')

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


def edit_exam_time_table(request, exam_pk):

    context = {}

    exam = Exam.objects.get(pk=exam_pk)

    context['exam'] = exam

    timetables = ExamTimeTable.objects.filter(exam=exam)

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

        exam = Exam.objects.get(pk=exam_pk)

        queryset = queryset.filter(exam=exam).order_by('date')
        return queryset

