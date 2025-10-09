# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Appointment, Thread, Message

# --- Custom User Admin ---

class CustomUserAdmin(UserAdmin):
    """Custom Admin for the User model."""
    # Add your custom fields to the fieldsets and list display
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'is_client')}),
    )
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'is_staff', 
        'is_client', 
        'phone_number'
    )
    search_fields = ('username', 'email', 'phone_number')

# Unregister the default User model if it was implicitly registered
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Register the custom User model
admin.site.register(User, CustomUserAdmin)

# ----------------------------------------------------------------------

# --- Appointment Admin ---

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Admin for Appointment Booking."""
    list_display = ('client', 'start_time', 'end_time', 'service', 'status')
    list_filter = ('status', 'service', 'start_time')
    search_fields = ('client__username', 'service')
    date_hierarchy = 'start_time'
    
    # Allow admins to manually change the status
    list_editable = ('status',)

# ----------------------------------------------------------------------

# --- Messaging Admin ---

class MessageInline(admin.TabularInline):
    """Allows messages to be viewed/added directly inside the Thread view."""
    model = Message
    extra = 1 # Show 1 empty form by default
    fields = ('sender', 'content', 'timestamp')
    readonly_fields = ('timestamp',)

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    """Admin for Message Threads."""
    list_display = ('subject', 'client', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('subject', 'client__username')
    
    # Include the MessageInline to show all messages in the thread detail view
    inlines = [MessageInline]

# You do not typically need to register the Message model separately 
# since it's managed via ThreadAdmin using MessageInline.