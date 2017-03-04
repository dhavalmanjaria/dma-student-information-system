from django.shortcuts import render, redirect
from .models import TimeTable
from curriculum.models import Course, Semester, Subject
from django.contrib.auth.decorators import login_required
import logging
from datetime import datetime
from collections import OrderedDict

LOG = logging.getLogger('app')


def select_semester(request):

    context = {}
    context['semester'] = Semester.objects.all()

    return render(request, 'timetable/select_semester.html', context)

def _get_weekday(d):
    weekdays = {
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday'
    }

    return weekdays[d]


def _get_sorted_times(semester):
    times = [x.start_time for x in TimeTable.objects.filter(
        semester=semester)]

    times = sorted(set(times), key=int)
    return times

def _get_sorted_days(semester):
    return set(
        [x.day_of_week for x in TimeTable.objects.filter(
            semester=semester).order_by('day_of_week')])


def _get_timetable(semester):
    days = _get_sorted_days(semester)
    times = [x.start_time for x in TimeTable.objects.filter(
        semester=semester)]

    times = sorted(set(times), key=int)

    timetable = OrderedDict()

    for d in days:
        row = timetable[_get_weekday(d)] = []

        for t in times:
            try:
                row += [x.subject.name for x in TimeTable.objects.filter(
                    day_of_week=d, start_time=t)]
            except AttributeError as at:
                LOG.debug("_get_timetable():" + str(at))
                row += [None for x in TimeTable.objects.filter(
                    day_of_week=d, start_time=t)]
                # Subject name is None probably because that timeslot
                # has no subjects yet.
        # timetable[_get_weekday(d)] = row

    return timetable

def view_timetable(request, pk):
    context = {}
    semester = Semester.objects.get(pk=pk)
    LOG.debug(semester)
    context['semester'] = semester
    times = _get_sorted_times(semester)

    timetable = _get_timetable(semester)
    LOG.debug(timetable)

    context['timetable'] = timetable
    context['formatted_times'] = [datetime.strptime(t, "%H%M") for t in times]

    return render(request, 'timetable/view_timetable.html', context)


@login_required
def edit_timetable(request, pk):
    """
    Edit a time table. Note: The success of this function relies heavily on
    the fact that the start_times are sorted in ascending order. The times
    must be strings representing a 24h format specifically to do this. This
    method may not be the most elegant way to do this, but it does work quite
    well.
    """
    semester = Semester.objects.get(pk=pk)
    days = _get_sorted_days(semester)
    times = _get_sorted_times(semester)

    LOG.debug("edit_TT: " + str(times))

    timetable = _get_timetable(semester)
    LOG.debug("edit_tt:" + str(timetable))

    # TODO: Write test to make sure order is preserved
    if request.method == "POST":
        for d in days:
            for sub, t in zip(request.POST.getlist(_get_weekday(d)), times):
                LOG.debug("saving:" + _get_weekday(d) + ", " + t + ", "+ sub)

                tt = TimeTable.objects.get(
                    semester=semester, day_of_week=d, start_time=t)
                tt.subject = Subject.objects.get(name=sub)
                tt.save()

        return redirect('view-timetable', pk=semester.pk)

    context = {}
    context['subjects'] = [s.name for s in semester.subject_set.all()]
    context['timetable'] = timetable
    context['times'] = times
    context['formatted_times'] = [datetime.strptime(t, "%H%M") for t in times]
    context['semester'] = semester

    return render(request, 'timetable/edit_timetable.html', context)


@login_required
def edit_times(request, pk):
    semester = Semester.objects.get(pk=pk)
    context = {}
    times = _get_sorted_times(semester)

    if request.method == "POST":
        hours = request.POST.get('hours')
        minutes = request.POST.get('minutes')
        ampm = request.POST.get('a')

        new = request.POST.get('new_lecture')

        new_time = datetime.strptime(
            hours + " " + minutes + " " + ampm, "%I %M %p")
        new_time = datetime.strftime(new_time, "%H%M")

        if request.POST.get('submit'):
            submit = request.POST.get('submit')

        if new:
            LOG.debug(new)
            days = set(
                [x.day_of_week for x in TimeTable.objects.filter(
                semester=semester)])

            if len(days) < 1:
                tt = TimeTable(semester=semester, day_of_week=1,
                               start_time=new_time, subject=None)
                tt.save()

            for d in days:
                tt = TimeTable(semester=semester, day_of_week=d,
                               start_time=new_time, subject=None)
                LOG.debug(tt.get_day_of_week_display() + ":" + tt.start_time)
                tt.save()

        if submit == "Save":
            new_time = None
            try:
                LOG.debug(new_time)
            except ValueError as ve:
                LOG.debug(ve)
                context['errors'] = """Please check that the values entered are in
                the format HH MM AM/PM, eg: 9 00 AM"""

            #TODO: should sanitize this
            old_time = times[int(request.POST.get('lecture_number'))]
            tt_set = TimeTable.objects.filter(
                semester=semester, start_time=old_time)

            for entry in tt_set:
                entry.start_time = new_time
                entry.save()

        if submit == "Delete":
            old_time = times[int(request.POST.get('lecture_number'))]
            LOG.debug(old_time)
            TimeTable.objects.filter(start_time=old_time).delete()

    times = _get_sorted_times(semester)  # new times
    context['semester'] = semester

    context['formatted_times'] = [datetime.strptime(t, "%H%M") for t in times]
    return render(request, 'timetable/edit_times.html', context)


@login_required
def edit_days(request, pk, day):
    semester = Semester.objects.get(pk=pk)
    context = {}
    context['semester'] = semester

    if request.method == "GET":
        days = _get_sorted_days(semester)
        if len(days) < 1:
            new_day = 1
        else:
            new_day = len(days) + 1

        if new_day > 7:
            context['errors'] = "Error: Cannot add more than 7 days"

        times = _get_sorted_times(semester)
        LOG.debug("editday: " + str(days))
        if len(times) < 1:
            return redirect('edit-times', pk=semester.pk)

        add_rem = request.GET.get('day')

        if day == 'add':
            for t in times:
                tt = TimeTable(semester=semester, day_of_week=new_day,
                               start_time=t)
                tt.save()

        if day == 'remove' and days is not None:
            new_day = len(days)  # last day added
            TimeTable.objects.filter(day_of_week=new_day).delete()

    return redirect('edit-timetable', pk=semester.pk)
