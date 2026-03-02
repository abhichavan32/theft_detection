"""
URL configuration for electricity_theft_detection project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('theft_detection.urls')),
]
