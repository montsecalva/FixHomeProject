from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Modelo de usuario personalizado
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('tenant', 'Tenant'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='tenant')

# Modelo para gestionar citas


class Appointment(models.Model):
    REPAIR_CHOICES = [
        ('plumbing', 'Plumbing'),
        ('electricity', 'Electricity'),
        ('carpentry', 'Carpentry'),
        ('other', 'Other'),
    ]

    tenant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tenant_appointments',
        limit_choices_to={'role': 'tenant'},
        null = True
    )
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='admin_appointments',
        limit_choices_to={'role': 'admin'},
        null = True
    )
    repair_type = models.CharField(max_length=20, choices=REPAIR_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    assigned_professional = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment {self.id} - {self.repair_type} for {self.tenant.username}"


# Modelo para mensajes entre usuarios
class message(models.Model):
    id = models.BigAutoField(primary_key=True)  # ID autoincremental
    date = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación
    content = models.TextField()  # Contenido del mensaje
    image = models.ImageField(upload_to='message_images/', null=True, blank=True)  # Imagen opcional
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_messages',
        null=True
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        null=True

    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Message {self.id} - Created by {self.creator} for {self.recipient}"

