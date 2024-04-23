from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.professor_login, name='professor_login'),
    path('dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('logout/', views.professor_logout, name='professor_logout'),
    path('mycourses/', views.my_courses, name='my_courses'),
    path('course/<int:course_id>/', views.course_detail, name='course_details_prof'),
    path('course/<int:course_id>/add_student/', views.add_student_to_course, name='add_student_to_course'),
    path('create-announcement', views.announcement_view, name='announcement_view'),
    path('announcement/create/<int:course_id>/', views.create_announcement, name='create_announcement'),

]
