from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .decorators import professor_required
from base.models import Announcement, Course

def professor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('professor_dashboard')
        else:
            # Handle invalid login
            return render(request, 'professor_portal/login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'professor_portal/login.html')

def professor_logout(request):
    logout(request)
    return redirect('professor_login') 



@login_required
@professor_required
def professor_dashboard(request):
    courses = Course.objects.filter(course_incharge=request.user.professor)
    return render(request, 'professor_portal/dashboard.html', {'courses': courses})

@login_required
@professor_required
def my_courses(request):
    courses = Course.objects.filter(course_incharge=request.user.professor)
    return render(request, 'professor_portal/my_courses.html', {'courses': courses})

@professor_required
def course_detail(request, course_id):
    course = Course.objects.filter(id=course_id)
    return render(request, 'professor_portal/course_detail.html', {'course': course})
  

 
@login_required
@professor_required
def announcement_view(request):
    return render(request,'professor_portal/create_announcement.html')

@login_required
@professor_required
def create_announcement(request, course_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        files = request.FILES.getlist('files')
        
        course = Course.objects.get(id=course_id)
        
        announcement = Announcement.objects.create(
            title=title,
            content=content,
            course=course,
            created_by=request.user.professor  # Assuming each announcement is created by a professor
        )
        
        for file in files:
            announcement.files.create(file=file)
            
        return redirect('professor_dashboard')  # Redirect to dashboard after creating announcement
    else:
        course = Course.objects.get(id=course_id)
        return render(request, 'professor_portal/create_announcement.html', {'course': course})
