
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('base.urls')),
    path('professor/', include('professor_portal.urls')),
    path('accounts/', include('allauth.urls')),
]
