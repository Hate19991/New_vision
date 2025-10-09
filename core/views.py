# core/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import Appointment, Thread, Message, User
from .serializers import (
    AppointmentSerializer, ThreadDetailSerializer, MessageSerializer
)

# --- Permissions ---

class IsClientOrAdmin(permissions.BasePermission):
    """Allows access to clients (for their own data) or staff (for all data)."""
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        if isinstance(obj, Appointment) or isinstance(obj, Thread):
            return obj.client == request.user
        return False

# --- 1. Appointment ViewSet ---

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientOrAdmin]

    def get_queryset(self):
        """Filter appointments by the logged-in user unless they are staff."""
        if self.request.user.is_staff:
            return Appointment.objects.all()
        return Appointment.objects.filter(client=self.request.user)

    def perform_create(self, serializer):
        """Set the client automatically to the logged-in user."""
        serializer.save(client=self.request.user)

# --- 2. Messaging ViewSets ---

class ThreadViewSet(viewsets.ModelViewSet):
    serializer_class = ThreadDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientOrAdmin]
    
    def get_queryset(self):
        """Clients see only their threads. Staff sees all."""
        if self.request.user.is_staff:
            return Thread.objects.all().order_by('-updated_at')
        return Thread.objects.filter(client=self.request.user).order_by('-updated_at')

    def perform_create(self, serializer):
        """Set the client automatically to the logged-in user for new threads."""
        serializer.save(client=self.request.user)

    @action(detail=True, methods=['post'], url_path='send-message')
    def send_message(self, request, pk=None):
        thread = self.get_object()
        
        # Check if the user is the client of the thread or is staff/admin
        if thread.client != request.user and not request.user.is_staff:
            return Response({"detail": "You do not have permission to send a message to this thread."},
                            status=status.HTTP_403_FORBIDDEN)
                            
        # Ensure 'content' is provided
        content = request.data.get('content')
        if not content:
            return Response({"content": "This field is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create the message
        message = Message.objects.create(
            thread=thread,
            sender=request.user,
            content=content
        )
        
        serializer = MessageSerializer(message)
        # Update thread 'updated_at' time
        thread.save() 
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)