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
]

