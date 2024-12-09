from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('tenant', 'Tenant'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='tenant')

class Appointment(models.Model):
    REPAIR_CHOICES = [
        ('plumbing', 'Plumbing'),
        ('electricity', 'Electricity'),
        ('carpentry', 'Carpentry'),
        ('other', 'Other'),
    ]
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'tenant'})
    repair_type = models.CharField(max_length=20, choices=REPAIR_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=15,  # Incrementa el valor de max_length
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rescheduled', 'Rescheduled'),
        ],
        default='pending'
    )
    assigned_professional = models.CharField(max_length=50, blank=True, null=True)

