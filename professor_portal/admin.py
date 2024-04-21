from django.contrib import admin
from base.models import Course, Professor, Enrollment, Announcement,Eval,EvalMarks
from django.contrib.admin import AdminSite

class ProfessorAdminSite(AdminSite):
    site_header = 'Professor Admin'
    site_title = 'Professor Admin Portal'
    index_title = 'Welcome to the Professor Admin Portal'

professor_admin_site = ProfessorAdminSite(name='professor_admin')

# Register models with professor admin site
professor_admin_site.register(Course)
professor_admin_site.register(Professor)
professor_admin_site.register(Enrollment)
professor_admin_site.register(Announcement)
professor_admin_site.register(Eval)
professor_admin_site.register(EvalMarks)
