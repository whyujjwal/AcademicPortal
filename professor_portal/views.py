from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import professor_required
from base.models import Announcement, Course, Student, Enrollment
from .models import *
from .forms import StudentSearchForm, CourseForm, EvalForm
from django.urls import reverse



def professor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('professor_dashboard')
        else:
            
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


@login_required
@professor_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('professor_dashboard')  
    else:
        form = CourseForm()
    return render(request, 'professor_portal/add_course.html', {'form': form})
 
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

@login_required
@professor_required
def add_student_to_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = Student.objects.all()
    if request.method == 'POST':
        form = StudentSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            students = students.filter(name__icontains=search_query)
    else:
        form = StudentSearchForm()
    return render(request, 'professor_portal/add_student_to_course.html', {'course_id':course_id,'course': course, 'form': form, 'students': students})

@login_required
@professor_required
def add_student_process(request, course_id, student_id):
    course = get_object_or_404(Course, id=course_id)
    student = get_object_or_404(Student, id=student_id)
    TempCourseStudents.objects.create(course=course, student=student)

    return redirect('add_student_to_course', course_id=course_id)


def remove_student_from_cart(request, course_id,cart_item_id):
    cart_item = get_object_or_404(TempCourseStudents, id=cart_item_id)
    cart_item.delete()
    return render(request, 'professor_portal/add_student_cart.html', {'course_id':course_id})

def add_students_to_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        cart_items = TempCourseStudents.objects.filter(course=course)

        for cart_item in cart_items:
            enrollment, created = Enrollment.objects.get_or_create(
                student=cart_item.student,
                course=course
            )

        cart_items.delete()

        return redirect('course_detail', course_id=course_id)
    else:
        return redirect('add_student_cart', course_id=course_id)


def add_student_cart(request, course_id):
    course = get_object_or_404(Course,id = course_id)
    cart_items = TempCourseStudents.objects.all()
    return render(request, 'professor_portal/add_student_cart.html', {'course_id':course_id, 'cart_items': cart_items})



def create_eval(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = EvalForm(request.POST)
        if form.is_valid():
            eval_instance = form.save(commit=False)
            eval_instance.course = course
            eval_instance.save()
            return redirect('professor_dashboard')  
    else:
        form = EvalForm()
    
    return render(request, 'professor_portal/create_eval.html', {'form': form, 'course': course})