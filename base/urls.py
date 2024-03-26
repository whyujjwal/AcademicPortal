from django.urls import path
from .import views
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    path('',views.Home,name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/<int:course_id>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('download/<int:announcement_id>/', views.download_file, name='download_file'),
    path('register/', views.register, name='register'),
    path('cart/', views.cart, name='cart'),
    path('save_cart/', views.save_cart, name='save_cart'),
    path('add_to_cart/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:course_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cgpa-calculator/', views.cgpa_calculator, name='cgpa_calculator'),
    path('calculate-cgpa/', views.calculate_cgpa, name='calculate_cgpa'),
    path('course/<int:course_id>/evals/', views.EvalListView.as_view(), name='evals'),
    
]

