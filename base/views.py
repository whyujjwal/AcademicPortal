from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.http import HttpResponse

def Home(response):
    return render(response,"base/home.html")

@login_required
def dashboard(request):
    try:
        enrollments = Enrollment.objects.filter(student=request.user)
        courses = [enrollment.course for enrollment in enrollments]
        return render(request, 'base/dashboard.html', {'courses': courses})
    except Student.DoesNotExist:
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
        context['evals'] = Eval.objects.filter(course=course)
        
        student = self.request.user
        try:
            eval_marks = EvalMarks.objects.filter(student=student, eval__course=course)
            context['eval_marks'] = eval_marks
        except EvalMarks.DoesNotExist:
            context['eval_marks'] = None
        

        return context
    

class EvalListView(ListView):
    model = Eval
    template_name = 'base/evals.html'
    context_object_name = 'evaluations'

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Eval.objects.filter(course__id=course_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs['course_id']
        context['course'] = Course.objects.get(id=course_id)
        return context
    

def download_file(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    file_path = announcement.files.path
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % announcement.files.name
        return response

def register(request):
    user = request.user
    student = user.student
  
    branch = student.branch
    branch_cdc_courses = []#try to add branch befroe registering the student
    if branch:
        branch_cdc_courses = branch.cdc_courses.all()

    if branch_cdc_courses:
        all_courses = Course.objects.exclude(pk__in=branch_cdc_courses.values_list('pk', flat=True))
    else:
        all_courses = Course.objects.all()

    cart, created = Cart.objects.get_or_create(user=user)
    if created:
        student.cart = cart
        student.save()

    cart_courses = student.cart.courses.all()
    return render(request, 'base/register.html', {'courses': all_courses, 'cart_courses': cart_courses})
    
def cart(request):
    user = request.user
    student = user.student
   
    if student.isregistered:
        messages.error(request, "You are already registered.")
        return redirect('dashboard')
    cart_courses = student.cart.courses.all() if hasattr(student, 'cart') else []
    return render(request, 'base/cart.html', {'cart_courses': cart_courses})

def add_to_cart(request, course_id):
    course = Course.objects.get(pk=course_id)
    user = request.user
    student = user.student
    if student.isregistered:
        messages.error(request, "You are already registered.")
        return redirect('dashboard')
    cart, created = Cart.objects.get_or_create(user=user)
    student.cart = cart
    student.save()
    student.cart.courses.add(course)
    return redirect('register')

def remove_from_cart(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    student = user.student
    if student.isregistered:
        messages.error(request, "You are already registered.")
        return redirect('dashboard')
    student = user.student
    student.cart.courses.remove(course)
    return redirect('register')

def save_cart(request):
    user = request.user
    cart_courses = user.cart.courses.all() if hasattr(user, 'cart') else []
    student = user.student
    if student.isregistered:
        messages.error(request, "You are already registered.")
        return redirect('dashboard')
    for course in cart_courses:
        Enrollment.objects.create(student=user, course=course)
    
    student.isregistered = True
    user.save()
    student.save()
    user.cart.courses.clear()
    return redirect('home')

def create_dummy_enrollments(user):
    
    enrollments = Enrollment.objects.filter(student=user)
    for enrollment in enrollments:
        DummyEnrollment.objects.create(
            student=enrollment.student,
            course=enrollment.course,
            grade=None  
        )
    
@login_required
def cgpa_calculator(request):
   
    user = request.user
    if not DummyEnrollment.objects.filter(student=user).exists():
        create_dummy_enrollments(user)

    
    dummy_enrollments = DummyEnrollment.objects.filter(student=user)
    grade_choices = [
        ('A', 'A'), ('A-', 'A-'), ('B', 'B'), ('B-', 'B-'),
        ('C', 'C'), ('C-', 'C-'), ('D', 'D'), ('E', 'E'), ('NC', 'No Credit')
    ]

    context = {
        'dummy_enrollments': dummy_enrollments,
        'grade_choices': grade_choices,
    }

    return render(request, 'base/cgpa_calculator.html', context)

def get_grade_value(grade):
    grade_values = {
        'A': 10.0, 'A-': 9.0, 'B': 8.0, 'B-': 7.0,
        'C': 6.0, 'C-': 5.0, 'D': 4.0, 'E': 2.0, 'NC': 0.0
    }
    return grade_values.get(grade, 0.0)


def calculate_cgpa(request):
    if request.method == 'POST':
        user = request.user
        dummy_enrollments = DummyEnrollment.objects.filter(student=user)
        total_points = 0.0
        total_credit_hours = 0

        for dummy_enrollment in dummy_enrollments:
            grade = request.POST.get(f'grades[{dummy_enrollment.id}]')
            if grade and grade != 'NC':  # Exclude courses with 'No Credit'
                course = dummy_enrollment.course
                credit_hours = course.credit
                grade_value = get_grade_value(grade)
                total_points += credit_hours * grade_value
                total_credit_hours += credit_hours

        if total_credit_hours > 0:
            cgpa = total_points / total_credit_hours
        else:
            cgpa = 0.0

        dummy_enrollments = DummyEnrollment.objects.filter(student=user)
        grade_choices = [
            ('A', 'A'), ('A-', 'A-'), ('B', 'B'), ('B-', 'B-'),
            ('C', 'C'), ('C-', 'C-'), ('D', 'D'), ('E', 'E'), ('NC', 'No Credit')
        ]

        context = {
            'dummy_enrollments': dummy_enrollments,
            'grade_choices': grade_choices,
            'cgpa': cgpa,
        }

        messages.success(request, f'CGPA calculated: {cgpa:.2f}')
        return render(request, 'base/cgpa_calculator.html', context)

    else:
        return redirect('cgpa_calculator')