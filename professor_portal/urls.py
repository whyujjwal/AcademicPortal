# professor_portal/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView
from .admin import professor_admin_site

urlpatterns = [
    path('login/', professor_admin_site.urls),
]
