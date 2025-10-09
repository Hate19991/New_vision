# appointment_system/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    # DJ-REST-AUTH for Login, Logout, User Details
    path('auth/', include('dj_rest_auth.urls')), 
    # DJ-REST-AUTH for Google Social Auth
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/google/', include('allauth.socialaccount.providers.google.urls'), name='google_login'), 
    
    # Core App URLs
    path('api/', include('core.urls')),
]