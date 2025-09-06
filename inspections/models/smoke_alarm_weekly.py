from django.db import models
from .base import BaseInspection

class SmokeAlarmWeeklyInspection(models.Model):
    inspection = models.ForeignKey(
        BaseInspection,
        on_delete=models.CASCADE,
        related_name='smoke_alarm_weekly',
    )
    
    
    # Alarm Condition Checks
    installed_condition_ok = models.BooleanField(
        default=False,
        verbose_name="Installation Condition OK",
        help_text="Is the smoke alarm properly installed and in good condition?"
    )
    alarm_functional = models.BooleanField(
        default=False,
        verbose_name="Alarm Functional",
        help_text="Is the smoke alarm functioning correctly?"
    )
    battery_replaced = models.BooleanField(
        default=False,
        help_text="Has the battery been replaced as needed?"
    )
    
    # Findings and Actions
    faults_identified = models.TextField(
        blank=True,
        null=True,
        verbose_name="Identified Faults",
        help_text="Description of any faults found during inspection"
    )
    action_taken = models.TextField(
        blank=True,
        null=True,
        help_text="Corrective actions taken to address identified faults"
    )
    
    # Verification
    management_book_initials = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Initials in the management book confirming inspection"
    )
    
    comments = models.TextField(
        blank=True,
        null=True,
        help_text="Additional comments about the smoke alarm inspection"
    )
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Weekly Smoke Alarm Check - {self.inspection.location or 'Unknown Location'}"
