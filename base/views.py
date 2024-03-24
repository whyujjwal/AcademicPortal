from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Student, Enrollment, Course, Announcement
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.http import HttpResponse

def Home(response):
    return render(response,"base/base.html")



@login_required
def dashboard(request):
    try:
       
        # Retrieve the enrollments for the student
        enrollments = Enrollment.objects.filter(student=request.user)
        
        # Extract the courses from the enrollments
        courses = [enrollment.course for enrollment in enrollments]
        
        return render(request, 'base/dashboard.html', {'courses': courses})
    except Student.DoesNotExist:
        # Handle the case where the student does not exist
        return render(request, 'student_not_found.html')
    

class CourseDetailView(DetailView):
    model = Course
    template_name = 'base/course.html'
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['announcements'] = Announcement.objects.filter(course=course)
        
        student = self.request.user.student
        try:
            enrollment = Enrollment.objects.get(student=self.request.user, course=course)
            context['enrollment'] = enrollment
        except Enrollment.DoesNotExist:
            context['enrollment'] = None

        return context
    
    
def download_file(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    file_path = announcement.files.path
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % announcement.files.name
        return response