from rest_framework import serializers
from inspections.models.medication_comprehensive import MedicationAuditComprehensiveInspection
from inspections.serializers.base_serializers import BaseInspectionSerializer
from inspections.models.base import BaseInspection, InspectionType, InspectionStatus

class  InitiateMedicationAuditSerializer(BaseInspectionSerializer):
    location = serializers.CharField(write_only=True, required=False)
    client_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = MedicationAuditComprehensiveInspection
        fields = [
            'id',
            'location',
            'client_name',
            # Medication Storage Section
            'medications_cabinet_securely_locked',
            'medication_cabinet_clean_no_spillages',
            'medications_have_opening_dates_original_labels',
            'medication_label_has_client_details',
            'medication_stored_correctly',
            # Documentation Section
            'current_marr_sheet_match_client_records',
            'marr_sheet_list_all_medications_prescribed',
            'gap_on_marr_sheet',
            'all_documentation_black_ink',
            # Controlled Drugs Section
            'control_drug_for_client',
            'controlled_drugs_stored_recorded_correctly_count_correct',
            # PRN Medications Section
            'prn_medications',
            'directives_for_prn_clear_comprehensive',
            # Administration Section
            'medications_administration_coded_on_marr_sheet',
            'records_of_refusal_gp_informed',
            # Special Medication Types
            'transdermal_patch_protocol_for_use',
            'client_take_any_blood_thinners_up_to_date_risk_assessment',
            # Medication Ordering Section
            'order_of_medication_done_monthly_basis',
            'returns_medication_recorded_correctly_returns_book',
            # Free Text Fields
            'missing_administration_why',
            'why_returns_medication_for_client',
            'any_additional_comments',
            'any_follow_up_requires_by_whom',
            'comments',
            'is_active'
        ]
        read_only_fields = ['id']
    
    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        # if user.role not in ['worker', 'inspector']:
        #     raise serializers.ValidationError("Only workers and inspectors can initiate audits.")

        # Extract location and client_name
        location = validated_data.pop('location', None)
        client_name = validated_data.pop('client_name', None)

        # Create BaseInspection
        inspection = BaseInspection.objects.create(
            inspection_type=InspectionType.MEDICATION_COMPREHENSIVE,
            location=location,
            client_name=client_name,
            created_by=user,
            submitted_by_role=user.role,
            status=InspectionStatus.PENDING,
        )

        # Create MedicationAuditComprehensiveInspection
        medication_audit = MedicationAuditComprehensiveInspection.objects.create(
            inspection=inspection,
            **validated_data
        )

        return medication_audit 

    
    def update(self, instance, validated_data):
        # Extract and update BaseInspection fields if provided
        location = validated_data.pop('location', None)
        client_name = validated_data.pop('client_name', None)
        inspection_date = validated_data.pop('inspection_date', None)
        
        # Update the related BaseInspection if any of these fields are provided
        if any([location, client_name, inspection_date]):
            inspection = instance.inspection
            if location is not None:
                inspection.location = location
            if client_name is not None:
                inspection.client_name = client_name
            if inspection_date is not None:
                inspection.inspection_date = inspection_date
            inspection.save()

        # Update the FireAlarmWeeklyInspection instance
        return super().update(instance, validated_data)

    
    def to_representation(self, instance):
        """Custom representation to include inspection data"""
        representation = super().to_representation(instance)
        representation['inspection'] = {
            'id': instance.inspection.id,
            'inspection_type': instance.inspection.inspection_type,
            'location': instance.inspection.location,
            'client_name': instance.inspection.client_name,
            'status': instance.inspection.status,
            'created_by': instance.inspection.created_by.id,
            'submitted_by_role': instance.inspection.submitted_by_role,
            'inspection_date': instance.inspection.inspection_date
        }
        return representation
# class ClientInfoSerializer(serializers.Serializer):
#     client_name = serializers.CharField()
#     client_id = serializers.CharField()


# class AuditMetadataSerializer(serializers.Serializer):
#     date_of_audit = serializers.DateField()
#     auditor_name = serializers.CharField()


# class MedicationStorageSerializer(serializers.Serializer):
#     medications_cabinet_securely_locked = serializers.BooleanField()
#     medication_cabinet_clean_no_spillages = serializers.BooleanField()
#     medications_have_opening_dates_original_labels = serializers.BooleanField()
#     medication_label_has_client_details = serializers.BooleanField()
#     medication_stored_correctly = serializers.BooleanField()


# class DocumentationSerializer(serializers.Serializer):
#     current_marr_sheet_match_client_records = serializers.BooleanField()
#     marr_sheet_list_all_medications_prescribed = serializers.BooleanField()
#     gap_on_marr_sheet = serializers.BooleanField()
#     all_documentation_black_ink = serializers.BooleanField()


# class ControlledDrugsSerializer(serializers.Serializer):
#     control_drug_for_client = serializers.BooleanField()
#     controlled_drugs_stored_recorded_correctly_count_correct = serializers.BooleanField()


# class PRNMedicationsSerializer(serializers.Serializer):
#     prn_medications = serializers.BooleanField()
#     directives_for_prn_clear_comprehensive = serializers.BooleanField()


# class AdministrationSerializer(serializers.Serializer):
#     medications_administration_coded_on_marr_sheet = serializers.BooleanField()
#     records_of_refusal_gp_informed = serializers.BooleanField()


# class SpecialMedicationSerializer(serializers.Serializer):
#     transdermal_patch_protocol_for_use = serializers.BooleanField()
#     client_take_any_blood_thinners_up_to_date_risk_assessment = serializers.BooleanField()


# class MedicationOrderingSerializer(serializers.Serializer):
#     order_of_medication_done_monthly_basis = serializers.BooleanField()
#     returns_medication_recorded_correctly_returns_book = serializers.BooleanField()


# class FreeTextFieldsSerializer(serializers.Serializer):
#     missing_administration_why = serializers.CharField(allow_blank=True, required=False)
#     why_returns_medication_for_client = serializers.CharField(allow_blank=True, required=False)
#     any_additional_comments = serializers.CharField(allow_blank=True, required=False)
#     any_follow_up_requires_by_whom = serializers.CharField(allow_blank=True, required=False)
#     comments = serializers.CharField(allow_blank=True, required=False)


# class StaffVerificationSerializer(serializers.Serializer):
#     staff_name = serializers.CharField()
#     staff_signature = serializers.CharField()




# class InitiateMedicationAuditSerializer(BaseInspectionSerializer):
#     class Meta(BaseInspectionSerializer.Meta):
#         model = MedicationAuditComprehensiveInspection
#         fields = BaseInspectionSerializer.Meta.fields + (
#             'client_info', 'audit_metadata', 'medication_storage',
#             'documentation', 'controlled_drugs', 'prn_medications',
#             'administration', 'special_medication', 'medication_ordering',
#             'free_text', 'staff_verification'
#         )
#         read_only_fields = BaseInspectionSerializer.Meta.read_only_fields

#     def create(self, validated_data):
#         request = self.context['request']
#         user = request.user

#         if user.role not in ['worker', 'inspector']:
#             raise serializers.ValidationError("Only workers and inspectors can initiate audits.")

#         # Extract nested data
#         client_data = validated_data.pop('client_info')
#         audit_metadata = validated_data.pop('audit_metadata')
#         medication_storage = validated_data.pop('medication_storage')
#         documentation = validated_data.pop('documentation')
#         controlled_drugs = validated_data.pop('controlled_drugs')
#         prn = validated_data.pop('prn_medications')
#         administration = validated_data.pop('administration')
#         special = validated_data.pop('special_medication')
#         ordering = validated_data.pop('medication_ordering')
#         free_text = validated_data.pop('free_text')
#         staff = validated_data.pop('staff_verification')

#         base_inspection = BaseInspection.objects.create(
#             inspection_type=BaseInspection.InspectionType.MEDICATION_AUDIT_COMPREHENSIVE,
#             created_by=user,
#             submitted_by_role=user.role,
#             status=BaseInspection.InspectionStatus.PENDING
#         )

#         combined_data = {
#             **client_data,
#             **audit_metadata,
#             **medication_storage,
#             **documentation,
#             **controlled_drugs,
#             **prn,
#             **administration,
#             **special,
#             **ordering,
#             **free_text,
#             **staff,
#             'inspection': base_inspection
#         }

#         return MedicationAuditComprehensiveInspection.objects.create(**combined_data)



class MedicationAuditReadSerializer(serializers.ModelSerializer):
    inspection = BaseInspectionSerializer(read_only=True)

    class Meta:
        model = MedicationAuditComprehensiveInspection
        fields = '__all__'
        read_only_fields = (
            'created_at', 'created_by', 'approval_status',
            'approved_by', 'Approval_date', 'is_active'
        )
