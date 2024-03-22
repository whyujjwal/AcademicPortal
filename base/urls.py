from django.urls import path
from .import views

urlpatterns = [
    path('',views.Home,name='home'),
    path('dashboard/', views.Dashboard,name = 'student_dashboard'),
   
]
