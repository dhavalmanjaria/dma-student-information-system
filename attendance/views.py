from django.shortcuts import render, redirect
from django.views import generic
from django.http import JsonResponse
from .models import Attendance
from curriculum.models import Semester, Course
from user_management.models.group_info import StudentInfo
from timetable.models import TimeTable
from collections import OrderedDict
from datetime import datetime
from actions.views import SelectCourseSemester
import logging

LOG = logging.getLogger('app')

def get_faculty_subject_list(request):
    """
    This function returns the subject that a user can edit / view attendance
    for
    """

    actions_view = SelectCourseSemester()
    options = actions_view.get_options(request)

    subjects = []

    for k in options.keys():
        for subs in options[k].values():
            for s in subs:
                subjects.append(s[1])

    return subjects

def get_semester_attendance_list(request, pk, date):
    """
    This view returns the attendance for a particular
    semester on a particular date. The template this
    renders also allows editing of attendance Though the template uses a form
    this view does not actually have a form object that it
    uses.
    """
    context = {}
    semester = Semester.objects.get(pk=pk)
    context['semester'] = semester
    context['date'] = date
    attendance = OrderedDict()
    date = datetime.strptime(date, "%Y-%m-%d")

    student_set = set(
        att.student for att in
        Attendance.objects.filter(date=date, lecture__semester=semester))

    for x in student_set:
        attendance[x] = {}

    faculty_subjects = get_faculty_subject_list(request)
    LOG.debug

    lecture_list = [l for l in TimeTable.objects.filter(
        semester=semester, day_of_week=date.isoweekday()).order_by(
        'start_time')]

    for x in student_set:
        for lect in lecture_list:
            attendance[x][lect] = Attendance.objects.get(
                student=x, date=date, lecture=lect).is_present

    # Display attendance in log
    for x in student_set:
        LOG.debug(x)
        for lect in lecture_list:
            LOG.debug("\t" + lect.subject.name + " : " + str(
                attendance[x][lect]))

    context['attendance_list'] = attendance
    context['subjects'] = [lect.subject.name for lect in lecture_list]
    context['faculty_subjects'] = faculty_subjects

    return render(request, 'attendance/attendance-list.html', context)


def save_attendance_list(request, pk, date):
    """
    This view is designed mostly to take a POST object and save whatever the
    attendance and redirect back to the attendance list
    """
    context = {}
    semester = Semester.objects.get(pk=pk)
    context['semester'] = semester
    context['date'] = date
    date = datetime.strptime(date, "%Y-%m-%d")
   
    student_set = set(
        att.student for att in
        Attendance.objects.filter(date=date, lecture__semester=semester))

    lecture_list = [l for l in TimeTable.objects.filter(
        semester=semester, day_of_week=date.isoweekday()).order_by(
        'start_time')]

    # Perhaps using JSON here is a better idea but CSRF validation doesn't
    # work with JSON. So that may be changed in the future but as of now this
    # works.
    if request.method == "POST":
        for std in student_set:
            for lect in lecture_list:
                presence = request.POST.get(
                    std.user.username + "[" + str(lect.pk) + "]")

                if presence == "true":  # JavaScript true
                    presence = True

                if presence == "false":  # JavaScript false
                    presence = False

                att = Attendance.objects.get(
                    student=std, lecture=lect, date=date,
                    lecture__semester=semester)

                att.is_present = presence
                att.save()

    return redirect('attendance-list',
                             pk = semester.pk, date=(str(date.date())))


class SelectAttendance(SelectCourseSemester):

    def post(self, request):

        semester = super(SelectAttendance, self).get_semester_from_post(
            request)

        context = {}

        context['semester'] = semester

        date = datetime.strptime(request.POST.get('date'), "%d/%m/%Y")

        return redirect('attendance-list', pk=semester.pk, date=(
            str(date.date())))

    def get(self, request):

        options = super(SelectAttendance, self).get_options(request)

        if request.is_ajax():
            return JsonResponse(options)

        return render(request, 'attendance/select-attendance.html')