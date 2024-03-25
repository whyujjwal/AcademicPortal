from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


  
class Department(models.Model):
    name = models.CharField(max_length=100)
    head_of_department = models.ForeignKey('Professor', on_delete=models.SET_NULL, null=True, blank=True, related_name='departments_headed')

    def __str__(self):
        return self.name

#validator for credit
    
def validate_positive_less_than_5(value):
    if value <= 0 or value >= 5:
        raise ValidationError("Value must be a positive integer less than 5")

class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    course_incharge = models.ForeignKey('Professor', on_delete=models.SET_NULL, null=True, blank=True, related_name='courses_incharge')
    credit = models.IntegerField(validators=[validate_positive_less_than_5])
    

    def __str__(self):
        return self.name

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='professors')

    def __str__(self):
        return self.name


class BranchCode(models.Model):
    code = models.CharField(max_length = 2)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    

class Branch(models.Model):
    name = models.CharField(max_length=100)
    cdc_courses = models.ManyToManyField(Course, related_name='branches', blank=True)
    branch_code = models.ForeignKey(BranchCode,on_delete=models.SET_NULL,null = True,blank = True)
    def __str__(self):
        return self.name
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) #name is student id 
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    isregistered = models.BooleanField(default=False)
    cart = models.OneToOneField('Cart', on_delete=models.CASCADE, null=True, blank=True)

    def get_student(self):
        try:
            return self.student
        except Student.DoesNotExist:
            return None

    def __str__(self):
        return self.name

#Grades
GRADE_CHOICES = [
    ('A', 'A'),
    ('A-', 'A-'),
    ('B', 'B'),
    ('B-', 'B-'),
    ('C', 'C'),
    ('C-', 'C-'),
    ('D', 'D'),
    ('E', 'E'),
    ('NC', 'No Credit'),
]

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES,null=True,blank = True)


    def __str__(self):
        return f"{self.student.username} - {self.course.name}"
    
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements')
    created_by = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='announcements_created')
    created_at = models.DateTimeField(auto_now_add=True)
    files = models.FileField(upload_to='announcements/', blank=True, null=True)

    def __str__(self):
        return self.title



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    courses = models.ManyToManyField(Course, related_name='carts')

    def __str__(self):
        return f"Cart for {self.user.username}"
    

class DummyEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.name}: {self.grade}"


class Evals(models.Model):
    enrollment = models.ForeignKey(Enrollment,on_delete=models.CASCADE)
    marks = models.DecimalField(max_digits=4, decimal_places=2,null = True,blank = True)
    name = models.CharField(max_length=50)