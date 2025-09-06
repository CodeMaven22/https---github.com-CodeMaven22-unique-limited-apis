from rest_framework import serializers
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from ..models import BaseInspection


class BaseInspectionSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = BaseInspection
        fields = ('id', 'inspection_type', 'location', 'client_name', 'status', ''
                 'created_by', 'created_by_name', 'submitted_by_role', 'inspection_date')
        read_only_fields = ('id', 'inspection_type', 'status', 'created_by', 
                           'submitted_by_role', 'inspection_date')

    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()  # This works if your CustomUser model has get_full_name()
        return None
    # def validate(self, attrs):
    #     if attrs.get('status') == BaseInspection.InspectionStatus.APPROVED and not attrs.get('approved_by'):
    #         raise ValidationError("Approved by field is required when status is approved.")
    #     return attrs

# INSPECTION CONDUCT
class ConductInspectionSerializer(serializers.ModelSerializer):
    inspection_comments = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = BaseInspection
        fields = [
            'id',
            'inspection_conducted_by',
            'inspection_date',
            'inspection_comments',
            'status',
        ]
        read_only_fields = ['id', 'inspection_conducted_by', 'inspection_date']

    def update(self, instance, validated_data):
        request = self.context['request']
        user = request.user

        # Role restriction
        if user.role not in ['inspector', 'admin']:
            raise serializers.ValidationError("Only inspectors or admins can conduct inspections.")
        
        # Prevent duplicate conduct
        if instance.inspection_conducted_by:
            raise serializers.ValidationError("Inspection has already been conducted.")

        # Set the conducted by and inspection date automatically
        instance.inspection_conducted_by = user
        instance.inspection_date = timezone.now()

        # Allow inspector/admin to add optional comments and change status
        instance.inspection_comments = validated_data.get('inspection_comments', '')
        instance.status = validated_data.get('status', BaseInspection.InspectionStatus.CONDUCTED)

        instance.save()
        return instance



class ApproveInspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseInspection
        fields = ['id', 'approval_comments', 'approval_status']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        request = self.context['request']
        user = request.user

        # Only admin can approve
        if user.role != 'admin':
            raise serializers.ValidationError("Only admins can approve inspections.")

        # Prevent duplicate approval
        if instance.approved_by:
            raise serializers.ValidationError("Inspection already approved.")

        instance.approved_by = user
        instance.approval_comments = validated_data.get('approval_comments', '')
        instance.approval_status = validated_data.get('approval_status', BaseInspection.ApprovalStatus.PENDING)
        instance.status = BaseInspection.InspectionStatus.APPROVED 
        instance.Approval_date = timezone.now()
        instance.save()

        return instance



# SEARCH AND FILTER
