# core/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AppointmentViewSet, ThreadViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'messages/threads', ThreadViewSet, basename='thread')

urlpatterns = [
    path('', include(router.urls)),
]