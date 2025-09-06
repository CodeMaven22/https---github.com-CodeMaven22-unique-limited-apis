from django.db import models
from audits.models import Auditor
from inspections.models.base import BaseInspection

class FireAlarmWeeklyInspection(models.Model):
    inspection = models.ForeignKey(BaseInspection, on_delete=models.CASCADE, related_name='fire_alarm_weekly')
    point_checked = models.CharField(max_length=100, blank=True, null=True)
    alarm_functional = models.BooleanField(default=False, blank=True, null=True)
    call_points_accessible = models.BooleanField(default=False, blank=True, null=True)
    emergency_lights_working = models.BooleanField(default=False, blank=True, null=True)
    faults_identified_details = models.TextField(blank=True, null=True)
    action_taken_details = models.TextField(blank=True, null=True)
    management_book_initials = models.CharField(max_length=100, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.point_checked}- {self.inspection.inspection_date }"


class FireAlarmAudit(models.Model):
    inspection = models.OneToOneField(FireAlarmWeeklyInspection, on_delete=models.CASCADE, related_name='fire_alarm_audit')
    auditor = models.ForeignKey(Auditor, on_delete=models.SET_NULL, null=True, blank=True, related_name='fire_alarm_audits')
    date_of_audit = models.DateField(blank=True, null=True)
    audit_comments = models.TextField(blank=True, null=True)
    audit_passed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.location} - {self.inspection.created_at.date()}"
