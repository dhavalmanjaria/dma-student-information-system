from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse
from .models import Attendance
from curriculum.models import Semester, Course
from user_management.models.group_info import StudentInfo
from collections import OrderedDict
from datetime import datetime
from .forms import SelectAttendanceForm
import logging

LOG = logging.getLogger('app')


def get_attendance_list(request, pk, date):
    context = {}
    semester = Semester.objects.get(pk=pk)
    context['semester'] = semester
    attendance = OrderedDict()

    for std in [att.student for att in Attendance.objects.filter(
            lecture__semester=semester)]:
        attendance[std] = [att.lecture.subject.name + ":" + str(att.is_present) for att in Attendance.objects.filter(
            lecture__semester=semester, student=std,
            date=datetime(2017, 3, 1))]

    context['attendance_list'] = attendance

    return render(request, 'attendance/attendance_list.html', context)


def select(request):
    context = {}
    semester = Semester.objects.all()
    course = Course.objects.all()
    context['course'] = course

    #TODO: Use a form
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