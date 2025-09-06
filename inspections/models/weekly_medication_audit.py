from django.db import models

class WeeklyMedicationAuditInspection(models.Model):
    inspection = models.ForeignKey( 'inspections.BaseInspection', on_delete=models.CASCADE, related_name='weekly_medication_audits')
    # Medication Storage Section
    medications_cabinet_securely_locked = models.BooleanField(default=False, help_text="Is the medication cabinet securely locked?")
    medication_cabinet_clean_no_spillages = models.BooleanField(default=False, verbose_name="Medication Cabinet Clean",help_text="Is the medication cabinet clean with no spillages?")
    medications_have_opening_dates_original_labels = models.BooleanField(default=False,verbose_name="Proper Medication Labeling", help_text="Do all medications have opening dates and original labels?")
    medication_label_has_client_details = models.BooleanField(default=False, help_text="Do medication labels include client details?")
    medication_stored_correctly = models.BooleanField(default=False,help_text="Are all medications stored correctly according to requirements?")

    # Documentation Section
    current_marr_sheet_match_client_records = models.BooleanField(default=False, verbose_name="MARR Sheet Accuracy",help_text="Does the current MARR sheet match client records?")
    marr_sheet_list_all_medications_prescribed = models.BooleanField(default=False, verbose_name="Complete MARR Sheet",help_text="Does the MARR sheet list all prescribed medications?")
    gap_on_marr_sheet = models.BooleanField(default=False, help_text="Are there any gaps in the MARR sheet documentation?")
    boxed_bottled_medications_stock_count_entered = models.BooleanField(
        default=False,
        verbose_name="Stock Count Entered",
        help_text="Are stock counts entered for boxed/bottled medications?"
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
    prn_medications = models.BooleanField(default=False, verbose_name="PRN Medications Present", help_text="Are there any PRN (as-needed) medications?")
    directives_for_prn_clear_comprehensive = models.BooleanField( default=False, verbose_name="Clear PRN Directives", help_text="Are directives for PRN medications clear and comprehensive?")

    # Medication Administration Section
    medication_count_accurate = models.BooleanField(default=False, help_text="Is the medication count accurate?")
    medication_expiry_checked = models.BooleanField(default=False, help_text="Have medication expiry dates been checked?")
    missing_administration_why = models.TextField( blank=True, null=True, verbose_name="Missing Administration Reason", help_text="Explanation for any missing administrations")

    # Audit Findings
    any_issues = models.TextField(blank=True,null=True, help_text="Any issues identified during the audit")

    # Verification
    comments = models.TextField(blank=True, null=True, help_text="Additional comments about the audit")
    is_active = models.BooleanField(default=True, help_text="Is this audit active?")

    def __str__(self):
        return f"Weekly Medication Audit - {self.inspection.inspection_type} ({self.inspection.created_at})"

    class Meta:
        verbose_name = "Weekly Medication Audit"
        verbose_name_plural = "Weekly Medication Audits"
        ordering = ['-inspection__created_at']