from rest_framework import serializers
from inspections.models import FirstAidChecklistInspection, FirstAidChecklistItem
from inspections.serializers.base_serializers import BaseInspectionSerializer
from inspections.models.base import BaseInspection, InspectionStatus, InspectionType
from django.utils import timezone


class FirstAidChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstAidChecklistItem
        fields = ['id', 'item_name', 'quantity', 'available']


class InitiateFirstAidChecklistSerializer(serializers.ModelSerializer):
    location = serializers.CharField(write_only=True, required=True)
    client_name = serializers.CharField(write_only=True, required=True)
    items = FirstAidChecklistItemSerializer(many=True)
    
    class Meta:
        model = FirstAidChecklistInspection
        fields = ['id', 'location', 'client_name', 
                 'first_aid_kit_location', 'comments', 'items']
        read_only_fields = ['id']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        items_data = validated_data.pop('items')
        location = validated_data.pop('location')
        client_name = validated_data.pop('client_name')

        inspection = BaseInspection.objects.create(
            inspection_type=InspectionType.FIRST_AID,
            location=location,
            client_name=client_name,
            created_by=user,
            submitted_by_role=user.role,
            status=InspectionStatus.PENDING,
            inspection_date=timezone.now()
        )

        checklist = FirstAidChecklistInspection.objects.create(
            inspection=inspection,
            **validated_data
        )

        FirstAidChecklistItem.objects.bulk_create(
            FirstAidChecklistItem(checklist=checklist, **item)
            for item in items_data
        )
        return checklist

class FirstAidCheckListReadSerializer(serializers.ModelSerializer):
    items = FirstAidChecklistItemSerializer(many=True, read_only=True)

    class Meta:
        model = FirstAidChecklistInspection
        fields = [
            'id',
            'inspection',
            'first_aid_kit_location',
            'comments',
            'items',
        ]
        read_only_fields = ['id', 'inspection', 'date_of_inspection', 'comments']
    