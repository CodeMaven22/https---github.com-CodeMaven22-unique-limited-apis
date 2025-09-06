from rest_framework import serializers
from inspections.models.smoke_alarm_weekly import SmokeAlarmWeeklyInspection
from inspections.serializers.base_serializers import BaseInspectionSerializer
from inspections.models.base import BaseInspection, InspectionStatus, InspectionType

class SmokeAlarmWeeklySerializer(serializers.ModelSerializer):
    location = serializers.CharField(write_only=True, required=True)
    client_name = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = SmokeAlarmWeeklyInspection
        exclude = ('inspection',)  # Cleaner than listing all fields
        read_only_fields = ['id']

    def validate(self, data):
        """Validate required fields"""
        if not data.get('location') or not data.get('client_name'):
            raise serializers.ValidationError("Location and client name are required")
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required")

        user = request.user
        location = validated_data.pop('location')
        client_name = validated_data.pop('client_name')

        # Create base inspection
        base_inspection = BaseInspection.objects.create(
            inspection_type=InspectionType.SMOKE_ALARM,  # Fixed type
            location=location,
            client_name=client_name,
            created_by=user,
            submitted_by_role=user.role,
            status=InspectionStatus.PENDING,
        )

        # Create smoke alarm inspection
        inspection = SmokeAlarmWeeklyInspection.objects.create(
            inspection=base_inspection,
            **validated_data
        )
        return inspection
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
        """Include inspection details in response"""
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
class SmokeAlarmWeeklyInspectionReadSerializer(serializers.ModelSerializer):
    inspection = BaseInspectionSerializer(read_only=True)

    class Meta:
        model = SmokeAlarmWeeklyInspection
        fields = '__all__'
        read_only_fields = (
            'created_at', 'created_by', 'inspection_conducted_by', 
            'approval_status', 'approved_by', 'approval_date', 'is_active'
        )