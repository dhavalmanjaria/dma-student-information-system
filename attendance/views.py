from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from .models import Attendance
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from curriculum.models import Semester
from timetable.models import TimeTable
from collections import OrderedDict
from datetime import datetime
from actions.views import SelectCourseSemester
import logging

LOG = logging.getLogger('app')

# Why bother with strftime and datetime and everything when this is just fine?
# This does corresspond to the month numbers in python's datetime
MONTHS = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'Apri',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}


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

@login_required
@permission_required('user_management.can_read_attendance')
def get_student_attendance_list(request):

    requested_month = request.GET.get('month')

    context = {}
    current_month = datetime.now().month
    if requested_month:
        current_month = int(requested_month)

    context['current_month'] = current_month
    user = request.user

    attendance_list = Attendance.objects.filter(
        student=request.user.studentinfo)

    times = [x.start_time for x in TimeTable.objects.filter(
        semester=user.studentinfo.semester)]

    times = sorted(set(times), key=int)

    context['formatted_times'] = [datetime.strptime(
        t, "%H%M") for t in times]

    dates = set(
        [att.date for att in attendance_list if att.date.month == current_month])

    dates = sorted(dates)

    attendance_dict = OrderedDict()

    for d in dates:
        attendance_dict[d] = attendance_list.filter(
            date=d, student=user.studentinfo)

    context['attendance'] = attendance_dict

    context['months'] = MONTHS

    # Additional bells and whistles for this page
    total_lectures = len(dates) * len(times)
    attended_lectures = len([att.is_present for att in attendance_list.filter(
        is_present=True)])
    if total_lectures == 0:
        percentage_attended = "-"
    else:
        percentage_attended = round(attended_lectures / total_lectures * 100)

    context['total_lectures'] = total_lectures
    context['attended_lectures'] = attended_lectures
    context['percentage_attended'] = percentage_attended
    context['curr_month_name'] = MONTHS[current_month]

    return render(request,
                  'attendance/student-attendance-list.html', context)


@login_required
@permission_required('user_management.can_read_attendance')
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

@login_required
@permission_required('user_management.can_read_attendance')
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


class SelectAttendance(LoginRequiredMixin, PermissionRequiredMixin,
                       SelectCourseSemester):

    permission_required = ('user_management.can_read_attendance')

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
        LOG.debug(options)

        if request.is_ajax():
            return JsonResponse(options)

        return render(request, 'attendance/select-attendance.html')
   