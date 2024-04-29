from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import professor_required
from base.models import Announcement, Course, Student, Enrollment, EvalMarks
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

@login_required
@professor_required
def remove_student_from_cart(request, course_id,cart_item_id):
    cart_item = get_object_or_404(TempCourseStudents, id=cart_item_id)
    cart_item.delete()
    return render(request, 'professor_portal/add_student_cart.html', {'course_id':course_id})


@login_required
@professor_required
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



@login_required
@professor_required
def add_student_cart(request, course_id):
    course = get_object_or_404(Course,id = course_id)
    cart_items = TempCourseStudents.objects.all()
    return render(request, 'professor_portal/add_student_cart.html', {'course_id':course_id, 'cart_items': cart_items})


@login_required
@professor_required
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



@professor_required
def evaluate_students(request):
    students = Student.objects.all()
    initial_marks = {}
    if request.method == 'POST':
        for student in students:
            marks = request.POST.get(f"marks_{student.id}")
            if marks == '':
                marks = 0
            initial_marks[student.id] = int(marks)
         
            eval_marks, created = EvalMarks.objects.get_or_create(enrollment__student=student)
            eval_marks.marks = marks
            eval_marks.save()
    else:
        for student in students:
            initial_marks[student.id] = 0

    return render(request, 'professor_portal/eval_marks.html', {'students': students, 'initial_marks': initial_marks})


def save_eval_marks(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('marks_'):
                student_id = key.split('_')[1]
                marks = int(value)
                eval_marks, created = EvalMarks.objects.get_or_create(enrollment__student_id=student_id)
                eval_marks.marks = marks
                eval_marks.save()
    return redirect('evaluate_students') 



def evaluate_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    evals = Eval.objects.filter(course=course)
    return render(request, 'professor_portal/evaluate_course.html', {'course': course, 'evals': evals})

def give_marks(request, eval_id):
    # Your logic for giving marks for a particular evaluation goes here
    return redirect('evaluate_course', course_id=eval.course.id)