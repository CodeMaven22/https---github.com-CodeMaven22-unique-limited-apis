from rest_framework import serializers
from inspections.models import HealthSafetyChecklist
from inspections.models.base import BaseInspection, InspectionStatus, InspectionType
from inspections.serializers.base_serializers import BaseInspectionSerializer


class InitiateHealthSafetyChecklistSerializer(serializers.ModelSerializer):
    location = serializers.CharField(write_only=True)
    client_name = serializers.CharField(write_only=True)
    inspection_date = serializers.DateTimeField(write_only=True, required=False)  # Add this line

    
    class Meta:
        model = HealthSafetyChecklist
        exclude = ('inspection',)
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        
        # Extract location and client_name
        location = validated_data.pop('location')
        client_name = validated_data.pop('client_name')
        
        # Create BaseInspection
        inspection = BaseInspection.objects.create(
            inspection_type=InspectionType.HEALTH_SAFETY,
            location=location,
            client_name=client_name,
            created_by=user,
            submitted_by_role=user.role,
            status=InspectionStatus.PENDING,
        )
        
        # Create HealthSafetyChecklist
        checklist = HealthSafetyChecklist.objects.create(
            inspection=inspection,
            **validated_data
        )
        return checklist
    
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


class HealthSafetyChecklistReadSerializer(serializers.ModelSerializer):
    inspection = BaseInspectionSerializer(read_only=True)
    
    class Meta:
        model = HealthSafetyChecklist
        fields ='__all__'
        read_only_fields = (
            'created_at', 'created_by', 'inspection_conducted_by',
            'approval_status', 'approved_by', 'Approval_date', 'is_active'
        )
       