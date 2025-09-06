from django.db import models
from .base import BaseInspection

class MedicationAuditComprehensiveInspection(models.Model):
    inspection = models.ForeignKey( BaseInspection, on_delete=models.CASCADE, related_name='medication_audit_comprehensives')
    
    # Medication Storage Section
    medications_cabinet_securely_locked = models.BooleanField(default=False,help_text="Is the medication cabinet securely locked?")
    medication_cabinet_clean_no_spillages = models.BooleanField(
        default=False,
        verbose_name="Medication Cabinet Clean",
        help_text="Is the medication cabinet clean with no spillages?"
    )
    medications_have_opening_dates_original_labels = models.BooleanField(
        default=False,
        verbose_name="Proper Medication Labeling",
        help_text="Do all medications have opening dates and original labels?"
    )
    medication_label_has_client_details = models.BooleanField(
        default=False,
        help_text="Do medication labels include client details?"
    )
    medication_stored_correctly = models.BooleanField(
        default=False,
        help_text="Are all medications stored correctly according to requirements?"
    )
    
    # Documentation Section
    current_marr_sheet_match_client_records = models.BooleanField(
        default=False,
        verbose_name="MARR Sheet Accuracy",
        help_text="Does the current MARR sheet match client records?"
    )
    marr_sheet_list_all_medications_prescribed = models.BooleanField(
        default=False,
        verbose_name="Complete MARR Sheet",
        help_text="Does the MARR sheet list all prescribed medications?"
    )
    gap_on_marr_sheet = models.BooleanField(
        default=False,
        help_text="Are there any gaps in the MARR sheet documentation?"
    )
    all_documentation_black_ink = models.BooleanField(
        default=False,
        help_text="Is all documentation completed in black ink?"
    )
    
    # Controlled Drugs Section
    control_drug_for_client = models.BooleanField(
        default=False,
        verbose_name="Controlled Drugs Present",
        help_text="Are there any controlled drugs for this client?"
    )
    controlled_drugs_stored_recorded_correctly_count_correct = models.BooleanField(
        default=False,
        verbose_name="Controlled Drugs Properly Managed",
        help_text="Are controlled drugs stored, recorded, and counted correctly?"
    )
    
    # PRN Medications Section
    prn_medications = models.BooleanField(
        default=False,
        verbose_name="PRN Medications Present",
        help_text="Are there any PRN (as-needed) medications?"
    )
    directives_for_prn_clear_comprehensive = models.BooleanField(
        default=False,
        verbose_name="Clear PRN Directives",
        help_text="Are directives for PRN medications clear and comprehensive?"
    )
    
    # Administration Section
    medications_administration_coded_on_marr_sheet = models.BooleanField(
        default=False,
        verbose_name="Proper Administration Coding",
        help_text="Are medication administrations properly coded on MARR sheet?"
    )
    records_of_refusal_gp_informed = models.BooleanField(
        default=False,
        help_text="Are there records of medication refusal and GP notification?"
    )
    
    # Special Medication Types
    transdermal_patch_protocol_for_use = models.BooleanField(
        default=False,
        help_text="Is there a protocol for transdermal patch use?"
    )
    client_take_any_blood_thinners_up_to_date_risk_assessment = models.BooleanField(
        default=False,
        verbose_name="Blood Thinner Risk Assessment",
        help_text="Is there an up-to-date risk assessment for blood thinners?"
    )
    
    # Medication Ordering Section
    order_of_medication_done_monthly_basis = models.BooleanField(
        default=False,
        verbose_name="Monthly Medication Orders",
        help_text="Is medication ordering done on a monthly basis?"
    )
    returns_medication_recorded_correctly_returns_book = models.BooleanField(
        default=False,
        verbose_name="Proper Medication Returns",
        help_text="Are medication returns recorded correctly in the returns book?"
    )
    
    # Free Text Fields
    missing_administration_why = models.TextField(
        blank=True,
        null=True,
        help_text="Explanation for any missing administrations"
    )
    why_returns_medication_for_client = models.TextField(
        blank=True,
        null=True,
        help_text="Reason for medication returns for this client"
    )
    any_additional_comments = models.TextField(
        blank=True,
        null=True,
        help_text="Any additional comments about the medication audit"
    )
    any_follow_up_requires_by_whom = models.TextField(
        blank=True,
        null=True,
        help_text="Details of any required follow-up and responsible parties"
    )
    
    comments = models.TextField(
        blank=True,
        null=True,
        help_text="General comments about the audit"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates if the audit is active or has been soft deleted"
    )

    def __str__(self):
        return f"Medication Audit for - {self.inspection.client_name} by ({self.inspection.created_by}) on {self.inspection.created_at.date() if self.inspection else 'No Date'}"

    class Meta:
        verbose_name = "Comprehensive Medication Audit"
        verbose_name_plural = "Comprehensive Medication Audits"
        ordering = ['-inspection__created_at', '-inspection__client_name']