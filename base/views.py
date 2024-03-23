from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Student, Enrollment
from django.contrib.auth.models import User

def Home(response):
    return render(response,"base/base.html")

def Dashboard(response):
    return render(response,"base/student_dashboard.html")


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Student, Enrollment

@login_required
def dashboard(request):
    try:
        # Retrieve the currently logged-in user
        user = request.user

        # Ensure the user is an instance of User
        if not isinstance(user, User):
            raise ValueError("User must be an instance of User model")

        # Retrieve the associated student
        student = Student.objects.get(user=user)

        # Retrieve the enrollments for the student
        enrollments = Enrollment.objects.filter(student=student)

        # Extract the courses from the enrollments
        courses = [enrollment.course for enrollment in enrollments]

        return render(request, 'dashboard.html', {'courses': courses})
    except Student.DoesNotExist:
        # Handle the case where the student does not exist
        return render(request, 'student_not_found.html')
    except ValueError as ve:
        # Handle the case where the user is not an instance of User model
        return render(request, 'invalid_user.html', {'error_message': str(ve)})
