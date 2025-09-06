from django.db import models
from django.conf import settings
from core.models import UserRole

class InspectionStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"
    COMPLETED = "completed", "Completed"

class InspectionType(models.TextChoices):
    MEDICATION_COMPREHENSIVE = "medication_audit_comprehensive", "Medication Audit Comprehensive"
    WEEKLY_MEDICATION = "weekly_medication_audit", "Weekly Medication Audit"
    FIRE_ALARM = "fire_alarm_weekly", "Fire Alarm Weekly"
    SMOKE_ALARM = "smoke_alarm_weekly", "Smoke Alarm Weekly"
    WORKER = "worker_inspection", "Worker Inspection"
    HEALTH_SAFETY = "health_safety_checklist", "Health & Safety Checklist"
    FIRST_AID = "first_aid_checklist", "First Aid Checklist"


class BaseInspection(models.Model):
    inspection_type = models.CharField(max_length=40, choices=InspectionType.choices)
    location = models.CharField(max_length=255, blank=True, null=True,         help_text="Location of the smoke alarm being inspected")
    client_name = models.CharField(max_length=100, blank=True, null=True, help_text="Full name of the client being audited") 

    status = models.CharField(max_length=20, choices=InspectionStatus.choices, default=InspectionStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inspections") 
    submitted_by_role = models.CharField(max_length=20, choices=UserRole.choices)
    
    # INSPECTOR
    inspection_conducted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="inspected_inspections",
    )
    inspection_comments = models.TextField(blank=True)
    inspection_date = models.DateTimeField(null=True, blank=True)

    # APPROVAL BY ADMINS
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete = models.SET_NULL,
        related_name = "approved_inspections",
    )
    approval_comments = models.TextField(blank=True)
    Approval_date = models.DateTimeField(null=True, blank=True)

    def get_specific_checklist(self):
        """Get the type-specific checklist object if it exists"""
        for choice in InspectionType.values:
            if hasattr(self, choice):
                return getattr(self, choice)
        return None
    
    def __str__(self):
        return f"{self.inspection_type} - {self.client_name}"
