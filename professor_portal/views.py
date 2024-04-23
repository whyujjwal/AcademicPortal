from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import professor_required
from base.models import Announcement, Course, Student
from .forms import StudentSearchForm



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
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    
    return render(request, 'professor_portal/course_detail.html', {'course': course})


def add_student_to_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = StudentSearchForm(request.POST)
        if form.is_valid():
            # Get the search query from the form
            search_query = form.cleaned_data['search_query']
            # Perform a search for students based on the query
            students = Student.objects.filter(name__icontains=search_query)
            # Pass the search results to the template for display
            return render(request, 'professor_portal/add_student_to_course.html', {'course': course, 'students': students})
    else:
        form = StudentSearchForm()
    return render(request, 'professor_portal/add_student_to_course.html', {'course': course, 'form': form})

 
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
            created_by=request.user.professor  
        )
        
        for file in files:
            announcement.files.create(file=file)
            
        return redirect('professor_dashboard')  
    else:
        course = Course.objects.get(id=course_id)
        return render(request, 'professor_portal/create_announcement.html', {'course': course})
