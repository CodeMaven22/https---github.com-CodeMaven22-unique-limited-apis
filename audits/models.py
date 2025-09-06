from django.db import models

class Auditor(models.Model):
    INSPECTION_TYPE_CHOICES = [
        ('fire_alarm', 'Fire Alarm'),
        ('smoke_alarm', 'Smoke Alarm'),
        ('worker_inspection', 'Worker Inspection'),
        ('health_safety', 'Health & Safety'),
        ('first_aid', 'First Aid'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    organization = models.CharField(max_length=100, blank=True, null=True)
    assigned_inspection_types = models.JSONField(
        default=list,
        help_text="List of inspection types assigned to the auditor."
    )

    def __str__(self):
        return f"{self.name} - {self.organization or 'Independent'}"


class AuditRecord(models.Model):
    auditor = models.ForeignKey(Auditor, on_delete=models.SET_NULL, null=True, related_name="audits")
    date_of_audit = models.DateField()
    audit_comments = models.TextField(blank=True)
    audit_passed = models.BooleanField(default=True)

    class Meta:
        abstract = True
