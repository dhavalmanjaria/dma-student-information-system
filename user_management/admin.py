from django.contrib import admin

from .models import curriculum, all_permissions, group_info

admin.site.register(curriculum.Course)
admin.site.register(curriculum.Semester)
admin.site.register(curriculum.Subject)

