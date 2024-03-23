from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import Student

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        if sociallogin.account.provider == 'google':
            # Extract name from email
            email_parts = user.email.split('@')
            name = email_parts[0]
            # Create Student instance , if required the branch code can also be added 
            Student.objects.create(user=user, name=name)
        return user
