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

def register(request):
    user = request.user
    student = user.student
  
    branch = student.branch
    branch_cdc_courses = []
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


@login_required
def cgpa_calculator(request):

    user = request.user
    dummy_enrollments = DummyEnrollment.objects.filter(student=user)

    # Pass the dummy enrollments and grade choices to the template
    context = {
        'dummy_enrollments': dummy_enrollments,
        'grade_choices': GRADE_CHOICES,
    }

    
    return render(request, 'base/cgpa_calculator.html', {'cgpa': 0.0})



def calculate_cgpa(request):
    return HttpResponse("hi")

