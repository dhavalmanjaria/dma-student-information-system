from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    """
    Represents a course available in the college
    A course has semesters which in turn have subjects
    """
    long_name = models.CharField(max_length=200,
                                 help_text='The full name of the course')
    short_name = models.CharField(max_length=5,
                                  help_text='Short, abbreivated name'
                                  'that the course is referred by')

    #TODO: Change this to use FacultyInfo
    hod = models.OneToOneField(User, null=True)

    def __str__(self):
        return self.short_name


class Semester(models.Model):
    """
    Represents semesters as part of a course available. Each semester has
    subjects
    """
    course = models.ForeignKey(Course)
    semester_number = models.IntegerField()

    def _romanize(self, sem_no):
        roman = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
        if sem_no > 0 and sem_no < len(roman):
            return roman[sem_no - 1]

    def __str__(self):
        return str(self.course) + " " + self._romanize(self.semester_number)


class Subject(models.Model):
    """
    Represents subjects that are part of a semester in a course.
    """
    name = models.CharField(max_length=200, help_text='Name of the subject')
    semester = models.ForeignKey(Semester)
    faculty = models.ForeignKey('user_management.FacultyInfo',
                                null=True, blank=True)
    is_university_subject = models.BooleanField(default=True)

    def __str__(self):
        return self.name

