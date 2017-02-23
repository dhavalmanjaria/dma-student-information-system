from django.contrib import admin

from .models import all_permissions, group_info
from curriculum.models import Course, Semester, Subject

admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Subject)

