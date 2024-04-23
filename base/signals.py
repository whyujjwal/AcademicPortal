from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student, Enrollment, Announcement
from .utils import send_announcement_email

@receiver(post_save, sender=Student)
def handle_student_allocation(sender, instance, created,**kwargs):
    if created and instance.branch:
        branch_cdc_courses = instance.branch.cdc_courses.all()
        for course in branch_cdc_courses:
            Enrollment.objects.create(student=instance, course=course)


@receiver(post_save, sender=Announcement)
def send_announcement_notifications(sender, instance, created, **kwargs):
    if created:
     
        students = Student.objects.all()

        recipient_list = [student.user.email for student in students]
        subject = 'New Announcement: {}'.format(instance.title)
        message = 'Dear student,\n\nA new announcement "{}" has been posted. Please check it out.\n\nRegards,\Professor '.format(instance.title)
        send_announcement_email(subject, message, recipient_list)



#incase adapters doesn't works 
 
# @receiver(post_save, sender=User)
# def create_student_profile(sender, instance, created, **kwargs):
#     if created:
#         try:
#             # Check if the user was created via Google authentication
#             social_account = SocialAccount.objects.get(user=instance, provider='google')
#             if social_account:
#                 # Extract name from email
#                 email_parts = instance.email.split('@')
#                 name = email_parts[0]
#                 Student.objects.create(user=instance, name=name)
#         except SocialAccount.DoesNotExist:
#             pass