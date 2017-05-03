from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from user_management.models.auth_requests import AuthenticationRequest
from user_management.models.group_info import StudentInfo, FacultyInfo
from curriculum.models import Course, Semester, Subject
from django.views import View
from internal_assessment.models import StudentMetric, Metric
from university_credits.models import UniversityCredit, SubjectCredit
from notices.models import Notice
from examinations.models import Exam
from activity_log.models import Activity
from .forms import SelectSemesterForm
import logging

LOG = logging.getLogger('app')


def index(request):
    context = {}
    # Here we show the first five records for:
    # Notices
    # TimeTable
    # Activites
    # Assignments
    # Study Materials
    # Exam Schedule
    # Exam Hall Plan

    notices = Notice.objects.all().order_by('date')[:5]

    context['notices'] = notices
    context['activities'] = Activity.objects.all().order_by('date')[:5]
    context['exams'] = Exam.objects.first()

    return render(request, 'index.html', context)


@login_required
def dashboard(request):
    # TODO: Filter actions based on permissions

    if StudentInfo.objects.filter(user=request.user).first():  # User is student
        return render(request, 'student-dashboard.html')
    
    return render(request, 'dashboard.html')


class SelectCourseSemester(View):
    """
    This is a view that must be inherited by other views so that it gives the
    user the options to select a course and semester and other options based
    on what they're trying to do. The idea is to have a common view to select
    course and semester that adapts to the current action the user is trying
    to perform.
    """

    form = SelectSemesterForm()
    
    # The Select<App> template to render.
    select_template = ''

    # The view to redirect to after the user properly makes their choices
    redirect_to = ''

    # Additional context
    context = {}

    def get_semester_from_post(self, request):
        """
        Gets a semester object from the POST set
        """
        # TODO: Change this to actually use a pk
        semester = request.POST.get('semester')

        semester = [sem for sem in Semester.objects.all() if str(
                    sem) == semester][0]

        return semester

    def get_subject_from_post(self, request):
        """
        Gets a subject object from the POST set
        """
        subject_pk = request.POST.get('subject')

        subject = Subject.objects.get(pk=subject_pk)

        return subject

    subjects = []
    def get_options(self, request, all=False):
        user = request.user
        subjects = []

        if all:
            subjects = Subject.objects.all()

        else:
            try:
                LOG.debug(user)
                # User is faculty
                if FacultyInfo.objects.filter(user=user).first():
                    subjects = Subject.objects.filter(faculty=user.facultyinfo)

                # I'm trying to avoid checking if the user is assigned to a group
                # explicitly here because if in the future I want to add a different
                # group at the level of FacultyHOD, it would make things easier.

                # User is probably FacHOD
                if user.has_perm('user_management.can_auth_Faculty'):
                    # Subjects they teach
                    subjects = set([s for s in Subject.objects.filter(
                        faculty=user.facultyinfo)])

                    # But also all subjects in their course
                    courses = [user.facultyinfo.course, ]
                    for s in Subject.objects.filter(
                            semester__course__in=courses):
                        subjects.add(s)
                    LOG.debug(subjects)

            except Exception as ex:
                LOG.debug(str(ex))

            # User is Upper Management level
            if user.has_perm('user_management.can_auth_FacultyHOD'):
                # All subjects for all courses.
                subjects = Subject.objects.all()

            try:
                if StudentInfo.objects.filter(
                        user=user).first() is not None:  # User is student
                    LOG.debug("user: " + str(user.studentinfo))
                    semester = user.studentinfo.semester
                    subjects = Subject.objects.filter(semester=semester)
            except Exception as ex:
                LOG.debug(str(ex))

        semesters = set(Semester.objects.filter(subject__in=subjects))
        courses = set(Course.objects.filter(semester__in=semesters))

        options = {}

        for c in courses:
            options[c.short_name] = {}
        for sem in semesters:
            course_name = sem.course.short_name
            # options[course_name][(sem.pk, str(sem))] = []
            options[course_name][str(sem)] = []

        for sub in subjects:
            sem = str(sub.semester)
            course_name = sub.semester.course.short_name
            options[course_name][str(sem)].append((sub.pk, sub.name))

        return options

    def post(self, request):
        form = SelectSemesterForm(request.POST)

        if form.is_valid():

            semester = form.cleaned_data['semester']
            return redirect(self.redirect_to, semester.pk)
        else:
            self.context = {}
            self.context['errors'] = True
            self.context['form'] = form
        return render(request, self.select_template, self.context)

    def get(self, request):
        """
        This is just a demonstration of a standard implementation of this
        method
        """
        options = self.get_options(request)

        if request.is_ajax():
                return JsonResponse(options)

        return render(request, self.select_template, self.context)


# TODO: Move to own app, or at least the user_management app
@login_required
def auth_requests(request):
    """
    This view shows the authentication requests that the current user has the
    permission to grant
    """
    user = request.user
    can_auth_perms = [p.codename for p in user.user_permissions.filter(
        codename__startswith='can_auth_')]

    can_auth_groups = [n.replace('can_auth_', '') for n in can_auth_perms]

    all_requests = set(
        [r for r in AuthenticationRequest.objects.filter(
            group__name__in=can_auth_groups).filter(is_approved=False)])

    context = {}
    context['all_requests'] = all_requests

    return render(request, 'auth_requests.html', context)


def create_internal_assessment(user):
    """
    Saves internal assessment for a particular student. Used internally to
    create internal assessment for a newly registered user.
    """
    subjects = user.studentinfo.semester.subject_set.all()

    for sub in subjects:
        metrics = Metric.objects.filter(subject=sub)
        for m in metrics:
            smetric = StudentMetric(
                student=user.studentinfo, subject=sub, metric=m)
            smetric.marks = 0
            smetric.save()


def create_university_credits(user):
    """
    Saves university credtis for a particular student. Used internally to
    create university credits for a newly registered user.
    """
    subjects = user.studentinfo.semester.subject_set.all()

    for sub in subjects:
        crd = SubjectCredit.objects.get(subject=sub)
        smetric = UniversityCredit(
            student=user.studentinfo, credit=crd)
        smetric.marks = 0
        smetric.save()


@login_required
def grant_request(request):
    """
    This view processes an authentication request and grants the appropriate
    permissions. It does not return a template.
    """
    if request.method == "POST":
        auth_request = AuthenticationRequest.objects.get(pk=request.POST['pk'])
        auth_request.is_approved = True
        auth_request.save()

        user = auth_request.user
        group = auth_request.group

        perms = group.permissions.all()
        user.user_permissions.set(perms)

        LOG.debug("granted user: "+ str(user))

        # Also create University Credits and Internal Assessment records
        # if user is a student
        if StudentInfo.objects.filter(user=user).first():
            # Internal Assessment
            create_internal_assessment(user)
       
            # University Credits
            create_university_credits(user)

    return HttpResponse("view complete")
