from django.shortcuts import render, redirect
from .models import TimeTable
from curriculum.models import Course, Semester, Subject
import logging
from datetime import datetime

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

def _get_timetable(semester):
    days = set(
        [x.day_of_week for x in TimeTable.objects.filter(
            semester=semester)])
    times = [x.start_time for x in TimeTable.objects.filter(
        semester=semester)]

    times = sorted(set(times), key=int)

    timetable = []

    for d in days:
        row = []
        row.append(_get_weekday(d))
        for t in times:
            row += [x.subject.name for x in TimeTable.objects.filter(
                day_of_week=d, start_time=t)]
        timetable.append(row)

    return timetable

def view_timetable(request, pk):
    context = {}
    semester = Semester.objects.get(pk=pk)
    LOG.debug(semester)
    context['semester'] = semester
    times = [x.start_time for x in TimeTable.objects.filter(
        semester=semester)]

    times = sorted(set(times), key=int)

    timetable = _get_timetable(semester)
    LOG.debug(timetable)

    context['timetable'] = timetable
    context['formatted_times'] = [datetime.strptime(t, "%H%M") for t in times]

    return render(request, 'timetable/view_timetable.html', context)

def edit_timetable(request, pk):
    """
    Edit a time table. Note: The success of this function relies heavily on
    the fact that the start_times are sorted in ascending order. The times
    must be strings representing a 24h format specifically to do this. This
    method may not be the most elegant way to do this, but it does work quite
    well.
    """
    semester = Semester.objects.get(pk=pk)
    days = set(
        [x.day_of_week for x in TimeTable.objects.filter(
            semester=semester)])
    times = [x.start_time for x in TimeTable.objects.filter(
        semester=semester)]

    times = sorted(set(times), key=int)

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

        return redirect('view_timetable', pk=pk)

    context = {}
    context['subjects'] = [s.name for s in semester.subject_set.all()]
    context['timetable'] = timetable
    # context['times'] = times
    context['formatted_times'] = [datetime.strptime(t, "%H%M") for t in times]


    return render(request, 'timetable/edit_timetable.html', context)