from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals

class Department(models.Model):
    name = models.CharField(max_length=100)
    head_of_department = models.ForeignKey('Professor', on_delete=models.SET_NULL, null=True, blank=True, related_name='departments_headed')

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    course_incharge = models.ForeignKey('Professor', on_delete=models.SET_NULL, null=True, blank=True, related_name='courses_incharge')
    students = models.ManyToManyField('Student', related_name='courses', blank=True)

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
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Assign CDC courses to the student
        self.courses.set(self.branch.cdc_courses.all())
        super().save(*args, **kwargs)
    
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements')
    created_by = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='announcements_created')
    created_at = models.DateTimeField(auto_now_add=True)
    files = models.FileField(upload_to='announcements/', blank=True, null=True)

    def __str__(self):
        return self.title

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

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    grade = models.CharField(max_length=2,choices  = GRADE_CHOICES)

    def __str__(self):
        return f"{self.student.name} - {self.course.name}: {self.grade}"
    
