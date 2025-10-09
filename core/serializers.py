# core/serializers.py

from rest_framework import serializers
from .models import User, Appointment, Thread, Message
from dj_rest_auth.registration.serializers import RegisterSerializer

# --- Auth/User Serializers ---

class UserDetailsSerializer(serializers.ModelSerializer):
    """Used by dj-rest-auth for displaying authenticated user info."""
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'is_client')
        read_only_fields = ('email', 'username')


# --- Appointment Serializers ---

class AppointmentSerializer(serializers.ModelSerializer):
    client_username = serializers.CharField(source='client.username', read_only=True)

    class Meta:
        model = Appointment
        # Note: 'client' field will be set automatically in the view
        fields = ('id', 'client', 'client_username', 'start_time', 'end_time', 'service', 'status')
        read_only_fields = ('client', 'status')


# --- Messaging Serializers ---

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'sender_username', 'content', 'timestamp')
        read_only_fields = ('sender', 'thread', 'timestamp')

class ThreadDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    client_username = serializers.CharField(source='client.username', read_only=True)

    class Meta:
        model = Thread
        fields = ('id', 'client', 'client_username', 'subject', 'created_at', 'updated_at', 'messages')
        read_only_fields = ('client',)