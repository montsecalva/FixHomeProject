from django.contrib import admin
from .models import User, Appointment

# Registra el modelo User
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role',)
    search_fields = ('username', 'email')

# Registra el modelo Appointment
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'repair_type', 'date', 'time', 'status', 'assigned_professional')
    list_filter = ('status', 'repair_type', 'date')
    search_fields = ('tenant__username', 'assigned_professional')
