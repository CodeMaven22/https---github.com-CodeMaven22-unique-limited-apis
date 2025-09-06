from django.contrib import admin
from .models.base import BaseInspection
from .models.fire_alarm_weekly import FireAlarmWeeklyInspection
from .models.first_add_checklist import FirstAidChecklistInspection, FirstAidChecklistItem
from inspections.models import HealthSafetyChecklist
from .models.medication_comprehensive import MedicationAuditComprehensiveInspection
from .models.smoke_alarm_weekly import SmokeAlarmWeeklyInspection
from .models.health_safety_checklist import HealthSafetyChecklist
from .models.weekly_medication_audit import WeeklyMedicationAuditInspection


@admin.register(BaseInspection)
class BaseInspectionAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'location', 'inspection_type', 'created_at' )


    search_fields = ('location', 'client_name',  'inspection_type', 'status', 'created_by__email')
    # list_filter = ('inspection__location', 'inspection__client_name', 'inspection__inspection   _type', 'inspection__status')
    readonly_fields = ('created_at',)


@admin.register(FireAlarmWeeklyInspection)
class FireAlarmWeeklyInspectionAdmin(admin.ModelAdmin):
    list_display = ('get_client_name', 'get_location', 'get_inspection_type', 'get_status', 'get_created_at' )
    
    def get_client_name(self, obj):
        return obj.inspection.client_name
    get_client_name.short_description = 'Client Name'

    def get_location(self, obj):
        return obj.inspection.location
    get_location.short_description = 'Location'

    def get_inspection_type(self, obj):
        return obj.inspection.inspection_type
    get_inspection_type.short_description = 'Inspection Type'

    def get_status(self, obj):
        return obj.inspection.status
    get_status.short_description = 'Status'

    def get_created_at(self, obj):
        return obj.inspection.created_at
    get_created_at.short_description = 'Created At'

    search_fields = ('get_location', 'get_client_name',  'get_inspection_type', 'get_status', 'inspection__created_by__email')
    # list_filter = ('inspection__location', 'inspection__client_name', 'inspection__inspection   _type', 'inspection__status')
    readonly_fields = ('get_created_at',)




class FirstAidChecklistItemInline(admin.TabularInline):
    model = FirstAidChecklistItem
    extra = 1
    can_delete = False


@admin.register(FirstAidChecklistInspection)
class FirstAidChecklistInspectionAdmin(admin.ModelAdmin):
    list_display = ('get_client_name', 'get_location', 'get_inspection_type', 'get_status', 'get_created_at' )
    
    def get_client_name(self, obj):
        return obj.inspection.client_name
    get_client_name.short_description = 'Client Name'

    def get_location(self, obj):
        return obj.inspection.location
    get_location.short_description = 'Location'

    def get_inspection_type(self, obj):
        return obj.inspection.inspection_type
    get_inspection_type.short_description = 'Inspection Type'

    def get_status(self, obj):
        return obj.inspection.status
    get_status.short_description = 'Status'

    def get_created_at(self, obj):
        return obj.inspection.created_at
    get_created_at.short_description = 'Created At'

    search_fields = ('get_location', 'get_client_name',  'get_inspection_type', 'get_status', 'inspection__created_by__email')
    # list_filter = ('inspection__location', 'inspection__client_name', 'inspection__inspection   _type', 'inspection__status')
    readonly_fields = ('get_created_at',)
   
    inlines = [FirstAidChecklistItemInline]
    readonly_fields = ('created_at', 'updated_at')

    def created_at(self, obj):
        return obj.inspection.created_at

    def updated_at(self, obj):
        return obj.inspection.updated_at



@admin.register(HealthSafetyChecklist)
class HealthSafetyChecklistAdmin(admin.ModelAdmin):
    list_display = ('get_client_name', 'get_location', 'get_inspection_type', 'get_status', 'get_created_at' )
    
    def get_client_name(self, obj):
        return obj.inspection.client_name
    get_client_name.short_description = 'Client Name'

    def get_location(self, obj):
        return obj.inspection.location
    get_location.short_description = 'Location'

    def get_inspection_type(self, obj):
        return obj.inspection.inspection_type
    get_inspection_type.short_description = 'Inspection Type'

    def get_status(self, obj):
        return obj.inspection.status
    get_status.short_description = 'Status'

    def get_created_at(self, obj):
        return obj.inspection.created_at
    get_created_at.short_description = 'Created At'

    search_fields = ('get_location', 'get_client_name',  'get_inspection_type', 'get_status', 'inspection__created_by__email')
    # list_filter = ()
    # 'inspection__location', 'inspection__client_name', 'inspection__inspection   _type', 'inspection__status'
    readonly_fields = ('get_created_at',)

    fieldsets = (
        ('General Info', {
            'fields': (
                'inspection',
                'previous_concerns_addressed',
                'comments',
                'is_active',
            )
        }),
        ('Policy & Training', {
            'fields': (
                'policy_up_to_date_local_health_safety',
                'staff_issued_personal_copy_policy_told_text',
                'health_safety_standing_item_agenda_previous_staff_meeting',
                'all_staff_received_training_health_safety_procedures',
                'new_staff_receive_training_beginning_employment',
                'temporary_staff_receive_necessary_training',
            )
        }),
        ('Equipment & Workstation', {
            'fields': (
                'staff_carry_out_manual_handling_risk_assessment',
                'equipment_used_mobility_risk_assessment',
                'computer_workstation_assessments_carried_out_recorded',
                'working_conditions_suitable_noise_lighting_ventilation_temperature',
                'furniture_furnishings_good_condition_suitable_stable',
                'equipment_suitable_maintained_good_condition',
                'floor_surfaces_acceptable_condition',
            )
        }),
        ('Fire Safety', {
            'fields': (
                'fire_doors_kept_closed',
                'notices_informing_staff_what_to_do_fire',
                'staff_know_what_to_do_event_fire',
                'adequate_first_aiders_available',
                'easy_to_find_first_aiders',
            )
        }),
        ('Electrical Safety', {
            'fields': (
                'electricity_obvious_defects_electrical_equipment',
                'sockets_overloaded',
                'all_electrical_equipment_inspected',
                'circulation_routes_kept_clear_obstructions_wires_cables_boxes',
            )
        }),
        ('Chemicals & Hazards', {
            'fields': (
                'harmful_substances_in_use_precautions_agreed',
            )
        }),
        # ('Approval', {
        #     'fields': (
        #         'approved_by',
        #         'Approval_date',
        #     )
        # }),
    )


@admin.register(MedicationAuditComprehensiveInspection)
class MedicationAuditComprehensiveInspectionAdmin(admin.ModelAdmin):
    list_display = ('get_client_name', 'get_location', 'get_inspection_type', 'get_status', 'get_created_at' )
    
    def get_client_name(self, obj):
        return obj.inspection.client_name
    get_client_name.short_description = 'Client Name'

    
    def get_location(self, obj):
        return obj.inspection.location 
    get_location

    def get_inspection_type(self, obj):
        return obj.inspection.inspection_type
    get_inspection_type.short_description = 'Inspection Type'

    def get_status(self, obj):
        return obj.inspection.status
    get_status.short_description = 'Status'

    def get_created_at(self, obj):
        return obj.inspection.created_at
    get_created_at.short_description = 'Created At'

    search_fields = ('get_location', 'get_client_name',  'get_inspection_type', 'get_status', 'inspection__created_by__email')
    list_filter = ('inspection__location', 'inspection__client_name', 'inspection__inspection_type', 'inspection__status')
    readonly_fields = ('get_created_at',)

    fieldsets = (
        (None, {
            'fields': (
                'inspection',
                'medications_cabinet_securely_locked', 'medication_cabinet_clean_no_spillages',
                'medications_have_opening_dates_original_labels', 'medication_label_has_client_details',
                'medication_stored_correctly', 'current_marr_sheet_match_client_records',
                'marr_sheet_list_all_medications_prescribed', 'gap_on_marr_sheet',
                'all_documentation_black_ink', 'control_drug_for_client',
                'controlled_drugs_stored_recorded_correctly_count_correct', 'prn_medications',
                'directives_for_prn_clear_comprehensive', 'medications_administration_coded_on_marr_sheet',
                'records_of_refusal_gp_informed', 'transdermal_patch_protocol_for_use',
                'client_take_any_blood_thinners_up_to_date_risk_assessment',
                'order_of_medication_done_monthly_basis', 'returns_medication_recorded_correctly_returns_book',
                'missing_administration_why', 'why_returns_medication_for_client',
                'any_additional_comments', 'any_follow_up_requires_by_whom',
                'comments', 'is_active'
            )
        }),
    )

@admin.register(SmokeAlarmWeeklyInspection)
class SmokeAlarmWeeklyInspectionAdmin(admin.ModelAdmin):
    list_display = ('get_client_name', 'get_location', 'get_inspection_type', 'get_status', 'get_created_at' )
    
    def get_client_name(self, obj):
        return obj.inspection.client_name
    get_client_name.short_description = 'Client Name'

    
    def get_location(self, obj):
        return obj.inspection.location 
    get_location

    def get_inspection_type(self, obj):
        return obj.inspection.inspection_type
    get_inspection_type.short_description = 'Inspection Type'

    def get_status(self, obj):
        return obj.inspection.status
    get_status.short_description = 'Status'

    def get_created_at(self, obj):
        return obj.inspection.created_at
    get_created_at.short_description = 'Created At'

    search_fields = ('get_location', 'get_client_name',  'get_inspection_type', 'get_status', 'inspection__created_by__email')
    list_filter = ('inspection__location', 'inspection__client_name', 'inspection__inspection_type', 'inspection__status')
    readonly_fields = ('get_created_at',)

    fieldsets = (
        (None, {
            'fields': (
                'inspection', 'installed_condition_ok',
                'alarm_functional', 'battery_replaced', 'faults_identified',
                'action_taken', 'management_book_initials', 'comments', 'is_active'
            )
        }),
    )


@admin.register(WeeklyMedicationAuditInspection)
class WeeklyMedicationAuditInspectionAdmin(admin.ModelAdmin):
    list_display = ('get_client_name', 'get_location', 'get_inspection_type', 'get_status', 'get_created_at' )
    
    def get_client_name(self, obj):
        return obj.inspection.client_name
    get_client_name.short_description = 'Client Name'

    
    def get_location(self, obj):
        return obj.inspection.location 
    get_location.short_description = 'Location'

    def get_inspection_type(self, obj):
        return obj.inspection.inspection_type
    get_inspection_type.short_description = 'Inspection Type'

    def get_status(self, obj):
        return obj.inspection.status
    get_status.short_description = 'Status'

    def get_created_at(self, obj):
        return obj.inspection.created_at
    get_created_at.short_description = 'Created At'

    search_fields = ('get_location', 'get_client_name',  'get_inspection_type', 'get_status', 'inspection__created_by__email')
    # list_filter = ('inspection__location', 'inspection__client_name', 'inspection__inspection_type', 'inspection__status')
    readonly_fields = ('get_created_at',)

    fieldsets = (
        (None, {
            'fields': (
                'inspection', 
                'medications_cabinet_securely_locked',
                'medication_cabinet_clean_no_spillages', 'medications_have_opening_dates_original_labels',
                'medication_label_has_client_details', 'medication_stored_correctly',
                # Add all fields here as per the model definition
            )
        }),
    )

