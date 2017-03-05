from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse
from .models import Attendance
from curriculum.models import Semester, Course
from user_management.models.group_info import StudentInfo
from timetable.models import TimeTable
from collections import OrderedDict
from datetime import datetime
from .forms import SelectAttendanceForm
import logging

LOG = logging.getLogger('app')


def get_attendance_list(request, pk, date):
    """
    This view returns the attendance for a particular
    semester on a particular date. The template this
    renders also allows editing of attendance
    (as of 2017-03-05). Though the template uses a form
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

    lecture_list = [l for l in TimeTable.objects.filter(
        semester=semester, day_of_week=date.isoweekday()).order_by(
        'start_time')]

    for x in student_set:
        for lect in lecture_list:
            attendance[x][lect] = Attendance.objects.get(
                student=x, date=date, lecture=lect).is_present

    # Display attendance
    for x in student_set:
        LOG.debug(x)
        for lect in lecture_list:
            LOG.debug("\t" + lect.subject.name + " : " + str(
                attendance[x][lect]))

    context['attendance_list'] = attendance
    context['subjects'] = [lect.subject.name for lect in lecture_list]

    return render(request, 'attendance/attendance_list.html', context)


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
                if presence == "false": # JavaScript false
                    presence = False

                att = Attendance.objects.get(
                    student=std, lecture=lect, date=date,
                    lecture__semester=semester)

                att.is_present = presence
                att.save()

    return redirect('attendance-list',
                             pk = semester.pk, date=(str(date.date())))

def select(request):
    """
    This view renders a template that allows a user to select a date,
    course and a semester and redirects to the attendance list.
    """
    context = {}
    semester = Semester.objects.all()
    course = Course.objects.all()
    context['course'] = course

    #TODO: Use a form, maybe
    if request.method == "POST":

        course = request.POST.get('course')
        semesters = Semester.objects.filter(course__short_name=course)
            
        if request.is_ajax():
            response = ''
            for x in semesters:
                response += "<option>" + str(x) + "</option>"
            LOG.debug(response)
            return HttpResponse(response)

        else:
            semester = [semester for semester in semesters if str(
                semester) == request.POST.get('semester')][0]

            date = datetime.strptime(request.POST.get('date'), "%d/%m/%Y")
            context['pk'] = semester.pk
            context['date'] = str(date.date())
            #return render(request, 'attendance/attendance_list.html', context)

            return redirect('attendance-list',
                             pk = semester.pk, date=(str(date.date())))

    return render(request, 'attendance/select_attendance.html', context)