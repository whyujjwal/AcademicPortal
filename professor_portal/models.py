from django.db import models
from django.contrib.auth.models import  User
from base.models import Course, Student


class TempCourseStudents(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='temp_course_students')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.name} - {self.course.name}"

