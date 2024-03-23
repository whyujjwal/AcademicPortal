from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Student, Enrollment, Course
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView

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
    

def course_registration(request):
    courses = Course.objects.all()
    return render(request, 'course_registration.html', {'courses': courses})