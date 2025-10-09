# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

# --- 1. Custom User Model ---
class User(AbstractUser):
    # Additional fields for booking appointments
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_client = models.BooleanField(default=True) # Default clients; admins manually set to False/use permissions
    
    # Use email as the unique identifier
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.email or self.username

# --- 2. Appointment Model ---
class Appointment(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    service = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )
    
    class Meta:
        ordering = ['start_time']
        
    def __str__(self):
        return f"Appt for {self.client.username} on {self.start_time.date()}"


# --- 3. Messaging Models ---

class Thread(models.Model):
    """Represents a conversation thread between a client and admin."""
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_threads')
    subject = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Thread {self.id}: {self.subject} ({self.client.username})"

class Message(models.Model):
    """An individual message within a thread."""
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE) # Either client or admin
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg by {self.sender.username} in Thread {self.thread.id}"