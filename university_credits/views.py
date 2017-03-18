from django.shortcuts import render, redirect
from .models import UniversityCredit, SubjectCredit
from actions.views import SelectCourseSemester
from django.views import View
from django.http import JsonResponse
from user_management.models.group_info import StudentInfo
from curriculum.models import Subject, Semester
from django.contrib.auth.decorators import login_required, permission_required
import logging

LOG = logging.getLogger('app')


class SelectCredits(View):
    """
    View that allows users to select course and semester.
    """
    def get(self, request):
        action_view = SelectCourseSemester()

        options = action_view.get_options(request)

        if request.is_ajax():
            return JsonResponse(options)

        return render(
            request, 'university-credits/select-university-credits.html')

    def post(self, request):
        action_view = SelectCourseSemester()

        semester = action_view.get_semester_from_post(request)

        context = {}

        context['semester'] = semester

        credits = SubjectCredit.objects.filter(subject__semester=semester)

        # User has student info. Using this avoids raising an exception
        if StudentInfo.objects.filter(user=request.user).first():
            # Return student-university-credits
            pass

        return redirect('credits-list', semester_pk=semester.pk)


@login_required
@permission_required('user_management.can_write_university_credits')
def edit_credits_for_semester(request, semester_pk):
    """
    View allows user to set max credits for a subject
    """
    if request.method == "POST":
        credit_pk = request.POST.get('crd_pk')
        credit = SubjectCredit.objects.get(pk=credit_pk)
        new_max_credits = request.POST.get('max_credits')
        credit.max_credits = new_max_credits
        credit.save()

    context = {}
    semester = Semester.objects.get(pk=semester_pk)
    credits = SubjectCredit.objects.filter(
        subject__semester=semester).order_by('subject')

    LOG.debug(credits)

    context['credits'] = credits


    return render(
        request,
        'university-credits/edit-credits-for-semester.html',
        context)


@login_required
@permission_required('user_management.can_write_university_credits')
def edit_credits_for_student(request, std_pk):
    """
    View allows a FacultyHOD user and above to edit metrics for a student,
    for a particular subject
    """
    context = {}
    student = StudentInfo.objects.get(pk=std_pk)

    context['student'] = student

    LOG.debug(student)

    credits = UniversityCredit.objects.filter(student=student)
    context['credits'] = credits

    LOG.debug(credits)


    if request.method == "POST":
        crd_pk = request.POST.get('crd_pk')
        ucrd = UniversityCredit.objects.get(pk=crd_pk)
        new_credits = request.POST.get('std_credits')
        ucrd.marks = new_credits

        ucrd.save()
        return redirect('edit-credits-for-student', std_pk=student.pk)

    return render(
        request, 'university-credits/edit-credits-for-student.html', context)


def get_credit_list(request, semester_pk):
    context = {}

    semester = Semester.objects.get(pk=semester_pk)

    context['semester'] = semester

    credits = UniversityCredit.objects.filter(student__semester=semester)

    students = [credit.student for credit in credits]

    credits_dict = {}

    for std in students:
        credits_dict[std] = {}

    for std in students:
        for ucrd in UniversityCredit.objects.filter(student=std):
            credits_dict[std][ucrd.credit.subject] = ucrd.marks

    context['credits'] = credits_dict
    subjects = Subject.objects.filter(semester=semester)
    context['subjects'] = subjects

    for sub in subjects:
        LOG.debug(sub)

    return render(
        request,
        'university-credits/student-university-credits-table.html',
        context)
