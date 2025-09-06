from django.db import models
from core.models import User

class Inspector(models.Model):
    inspector = models.OneToOneField(User, on_delete=models.CASCADE,related_name="inspector_profile",
        help_text="The user account associated with this inspector")
    years_of_experience = models.PositiveIntegerField(default=0,
        help_text="Number of years of inspection experience")
    
    def __str__(self):
        return f"Inspector: {self.inspector.get_full_name()}"


class Admin(models.Model):
    PERMISSION_LEVELS = [
        ('full', 'Full Access'),
        ('limited', 'Limited Access'),
        ('reports', 'Reports Only'),
    ]

    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin_profile",
        help_text="The user account associated with this admin")
    
    office_location = models.CharField(max_length=100,
        help_text="Primary office location for this administrator")
    


    def __str__(self):
        return f"Admin: {self.admin.get_full_name()}"


class Worker(models.Model):
    SHIFT_CHOICES = [
        ('day', 'Day Shift (8am-4pm)'),
        ('evening', 'Evening Shift (4pm-12am)'),
        ('night', 'Night Shift (12am-8am)'),
        ('rotation', 'Rotating Shifts'),
    ]

    DEPARTMENT_CHOICES = [
        ('production', 'Production'),
        ('maintenance', 'Maintenance'),
        ('quality', 'Quality Control'),
        ('shipping', 'Shipping/Receiving'),
        ('other', 'Other'),
    ]

    worker = models.OneToOneField( User, on_delete=models.CASCADE, related_name="worker_profile",
        help_text="The user account associated with this worker")
    department = models.CharField(max_length=100,choices=DEPARTMENT_CHOICES,
        help_text="Department the worker is assigned to")
    shift_type = models.CharField(max_length=20, choices=SHIFT_CHOICES, default='day',
        help_text="The worker's regular shift schedule")
    shift_time = models.TimeField(blank=True, null=True, 
        help_text="Time when the worker's shift starts (if applicable)" )
    next_shift_start = models.DateTimeField( blank=True, null=True,
        help_text="Date and time of worker's next scheduled shift")
   
    hire_date = models.DateField(
        blank=True,
        null=True,
        help_text="Date when the worker was hired"
    )

    class Meta:
        ordering = ['department', 'shift_type']

    def __str__(self):
        return f"Worker: {self.worker.get_full_name()}"


class Client(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile",
        help_text="The user account associated with this client")
    company_name = models.CharField(max_length=100, blank=True, null=True,
        help_text="Name of the client's company or organization")
    age = models.PositiveIntegerField(blank=True, null=True,
        help_text="Age of the client (if applicable, e.g., for individual clients)")
    
  

    def __str__(self):
        return f"{self.client.first_name} - {self.client.last_name} ({self.client.email})"
