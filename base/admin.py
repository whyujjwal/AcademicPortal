from django.contrib import admin
from .models import *


admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Professor)
admin.site.register(Branch)
admin.site.register(Student)
admin.site.register(Announcement)
admin.site.register(Grade)
admin.site.register(BranchCode)
admin.site.register(Enrollment)