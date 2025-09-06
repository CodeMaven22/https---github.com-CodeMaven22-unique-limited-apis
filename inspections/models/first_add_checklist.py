from django.db import models
from .base import BaseInspection

class FirstAidChecklistInspection(models.Model):
    inspection = models.ForeignKey(BaseInspection, on_delete=models.CASCADE, related_name='first_aid_checklists')
    first_aid_kit_location = models.CharField(max_length=255, blank=True, null=True, help_text="Location where the first aid kit is stored")
    comments = models.TextField(blank=True, null=True, help_text="Any additional comments about the first aid inspection")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "First Aid Checklist"
        verbose_name_plural = "First Aid Checklists"

    def __str__(self):
        return f"First Aid Checklist - {self.first_aid_kit_location or 'Unknown Location'} - {self.inspection.created_at or 'No Date'}"


class FirstAidChecklistItem(models.Model):
    checklist = models.ForeignKey(FirstAidChecklistInspection, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField( max_length=255, help_text="Name of the first aid item")
    quantity = models.CharField(max_length=50, blank=True, null=True, help_text="Required/available quantity of the item")
    available = models.BooleanField(default=False, help_text="Whether the item is available in the required quantity")

    class Meta:
        verbose_name = "First Aid Item"
        verbose_name_plural = "First Aid Items"
        ordering = ['item_name']

    def __str__(self):
        return f"{self.item_name} - {'Available' if self.available else 'Not Available'}"

# class FirstAidCheckListAudit(models.Model):
#     inspection =models.OneToOneField(FirstAidChecklistInspection, on_delete=models.CASCADE, related_name=''):
