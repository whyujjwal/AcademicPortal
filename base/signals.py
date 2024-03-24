from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student, Enrollment

@receiver(post_save, sender=Student)
def handle_student_allocation(sender, instance, created):
    if created and instance.branch:
        branch_cdc_courses = instance.branch.cdc_courses.all()
        for course in branch_cdc_courses:
            Enrollment.objects.create(student=instance, course=course)
