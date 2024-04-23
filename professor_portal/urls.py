from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.professor_login, name='professor_login'),
    path('dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('logout/', views.professor_logout, name='professor_logout'),
    path('announcement/create/<int:course_id>/', views.create_announcement, name='create_announcement'),
]
