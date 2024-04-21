from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, Http404

def Home(response):
    return render(response, "base/home.html")

@login_required
def dashboard(request):
    try:
        student = request.user.student
        enrollments = Enrollment.objects.filter(student=student)
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
        context['student'] = self.request.user
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
        course = get_object_or_404(Course, id=course_id)

        try:
            student = self.request.user.student
            eval_marks = EvalMarks.objects.filter(enrollment__student=student, eval__course=course)
            eval_marks_dict = {eval_mark.eval_id: eval_mark for eval_mark in eval_marks}
            context['course'] = course
            context['eval_marks'] = eval_marks_dict
        except Student.DoesNotExist:
            context['eval_marks'] = {}
        return context

@login_required
def download_file(request, announcement_id):
    try:
        announcement = get_object_or_404(Announcement, id=announcement_id)
        file_path = announcement.files.path
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=%s' % announcement.files.name
            return response
    except Exception as e:
        messages.error(request, f"An error occurred while downloading file: {str(e)}")
        return redirect('home')

@login_required
def register(request):
    try:
        user = request.user
        student = user.student
    except Student.DoesNotExist:
        messages.error(request, "User does not have a corresponding Student instance.")
        return redirect('home')

    branch = student.branch
    branch_cdc_courses = branch.cdc_courses.all() if branch else []
    all_courses = Course.objects.exclude(pk__in=branch_cdc_courses.values_list('pk', flat=True)) if branch_cdc_courses else Course.objects.all()

    cart, created = Cart.objects.get_or_create(user=student)
    if created:
        student.cart = cart
        student.save()

    cart_courses = student.cart.courses.all()
    return render(request, 'base/register.html', {'courses': all_courses, 'cart_courses': cart_courses})

@login_required 
def cart(request):
    user = request.user
    student = user.student
    if student.isregistered:
        messages.error(request, "You are already registered.")
        return redirect('dashboard')
    cart_courses = student.cart.courses.all() if hasattr(student, 'cart') else []
    return render(request, 'base/cart.html', {'cart_courses': cart_courses})

@login_required
def add_to_cart(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        user = request.user
        student = user.student
        if student.isregistered:
            messages.error(request, "You are already registered.")  
            return redirect('dashboard')
        cart, created = Cart.objects.get_or_create(user=student)
        student.cart = cart
        student.save()
        student.cart.courses.add(course)
        return redirect('register')
    except Exception as e:
        messages.error(request, f"An error occurred while adding course to cart: {str(e)}")
        return redirect('home')

@login_required
def remove_from_cart(request, course_id):
    try:
        course = get_object_or_404(Course, pk=course_id)
        user = request.user
        student = user.student
        if student.isregistered:
            messages.error(request, "You are already registered.")
            return redirect('dashboard')
        student = user.student
        student.cart.courses.remove(course)
        return redirect('register')
    except Exception as e:
        messages.error(request, f"An error occurred while removing course from cart: {str(e)}")
        return redirect('home')

@login_required
def save_cart(request):
    try:
        user = request.user
        student = user.student
        cart_courses = student.cart.courses.all()  
        
        if student.isregistered:
            messages.error(request, "You are already registered.")
            return redirect('dashboard')

        for course in cart_courses:
            Enrollment.objects.create(student=student, course=course)

        student.isregistered = True
        student.save()
        student.student_cart.courses.clear()
        return redirect('home')
    except Student.DoesNotExist:
        messages.error(request, "Student record not found.")
        return redirect('home')
    except AttributeError:
        messages.error(request, "Cart not found for this user.")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"An error occurred while saving cart: {str(e)}")
        return redirect('home')


@login_required
def create_dummy_enrollments(request):
    try:
        student = get_object_or_404(Student, user=request.user)
        enrollments = Enrollment.objects.filter(student=student)
        for enrollment in enrollments:
            DummyEnrollment.objects.create(
                student=enrollment.student,
                course=enrollment.course,
                grade=None
            )
        messages.success(request, "Dummy enrollments created successfully.")
    except Http404:
        messages.error(request, "Student record not found.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    return redirect('cgpa_calculator')

@login_required
def cgpa_calculator(request):
    try:
        user = request.user
        if not DummyEnrollment.objects.filter(student__user=user).exists():
            create_dummy_enrollments(request)

        dummy_enrollments = DummyEnrollment.objects.filter(student__user=user)
        grade_choices = [('A', 'A'), ('A-', 'A-'), ('B', 'B'), ('B-', 'B-'), ('C', 'C'), ('C-', 'C-'), ('D', 'D'), ('E', 'E'), ('NC', 'No Credit')]
        context = {'dummy_enrollments': dummy_enrollments, 'grade_choices': grade_choices}
        return render(request, 'base/cgpa_calculator.html', context)
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')

def get_grade_value(grade):
    grade_values = {'A': 10.0, 'A-': 9.0, 'B': 8.0, 'B-': 7.0, 'C': 6.0, 'C-': 5.0, 'D': 4.0, 'E': 2.0, 'NC': 0.0}
    return grade_values.get(grade, 0.0)

@login_required
def calculate_cgpa(request):
    if request.method == 'POST':
        try:
            student = get_object_or_404(Student, user=request.user)
            dummy_enrollments = DummyEnrollment.objects.filter(student=student)
            total_points = 0.0
            total_credit_hours = 0
           
            for dummy_enrollment in dummy_enrollments:
                grade = request.POST.get(f'grades[{dummy_enrollment.id}]')
                if grade and grade != 'NC': 
                    course = dummy_enrollment.course
                    credit_hours = course.credit
                    grade_value = get_grade_value(grade)  
                    total_points += credit_hours * grade_value
                    total_credit_hours += credit_hours
            
            if total_credit_hours > 0:
                cgpa = total_points / total_credit_hours
                cgpa = "{:.2f}".format(cgpa)
            else:
                cgpa = 0.0
        
            dummy_enrollments = DummyEnrollment.objects.filter(student=student)
            grade_choices = [('A', 'A'), ('A-', 'A-'), ('B', 'B'), ('B-', 'B-'), ('C', 'C'), ('C-', 'C-'), ('D', 'D'), ('E', 'E'), ('NC', 'No Credit')]
            context = {'dummy_enrollments': dummy_enrollments, 'grade_choices': grade_choices, 'cgpa': cgpa}
            messages.success(request, f'CGPA calculated: {cgpa:.2f}')
            return render(request, 'base/cgpa_calculator.html', context)
        except Http404:
            messages.error(request, "Student record not found.")
            return redirect('cgpa_calculator')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('cgpa_calculator')
    else:
        return redirect('cgpa_calculator')
