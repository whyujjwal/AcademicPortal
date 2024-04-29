from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.professor_login, name='professor_login'),
    path('dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('logout/', views.professor_logout, name='professor_logout'),
    path('mycourses/', views.my_courses, name='my_courses'),
    path('addcourse/',views.add_course,name='add_course'),
    path('course/<int:course_id>/', views.course_detail, name='course_details_prof'),
    path('course/<int:course_id>/add_student/', views.add_student_to_course, name='add_student_to_course'),
    path('course/<int:course_id>/add-student/<int:student_id>/',views.add_student_process, name='add_student_process'),
    path('course/<int:course_id>/remove-student/<int:cart_item_id>/', views.remove_student_from_cart, name='remove_student_from_cart'),
    path('course/<int:course_id>/add-students/', views.add_students_to_course, name='add_students_to_course'),
    path('add-student-cart/<int:course_id>/', views.add_student_cart, name='add_student_cart'),
    path('create-announcement', views.announcement_view, name='announcement_view'),
    path('announcement/create/<int:course_id>/', views.create_announcement, name='create_announcement'),
    path('course/<int:course_id>/create-eval/', views.create_eval, name='create_eval'),
    path('evaluate/', views.evaluate_students, name='evaluate_students'),
    path('save_eval_marks/', views.save_eval_marks, name='save_eval_marks'),

]
