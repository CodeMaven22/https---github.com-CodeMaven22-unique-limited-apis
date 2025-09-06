from inspections.serializers.medication_comprehensive_serializers import (
    InitiateMedicationAuditSerializer,
    MedicationAuditReadSerializer
)
from inspections.models.medication_comprehensive import MedicationAuditComprehensiveInspection
from core.permissions import IsWorkerOrInspector, IsInspectorOrAdmin, IsAdminOnly
from rest_framework import generics, permissions, status
from rest_framework.response import Response

# 1. Initiate or List Inspections (Workers or Inspectors)
class ListCreateMedicationAuditView(generics.ListCreateAPIView):
    queryset = MedicationAuditComprehensiveInspection.objects.filter(is_active=True)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # If user is not authenticated, return empty queryset
        if not user.is_authenticated:
            return MedicationAuditComprehensiveInspection.objects.none()
        
        # Admin can see all inspections
        if user.role == 'admin' or user.role == 'team_leader' or user.role == 'inspector':
            return queryset
        
        # Worker can only see their own inspections
        elif user.role == 'worker':
            return queryset.filter(inspection__created_by=user)
        
        # Default: return empty queryset for other roles
        return MedicationAuditComprehensiveInspection.objects.none()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return InitiateMedicationAuditSerializer
        return MedicationAuditReadSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

# 2. Retrieve / Update / Soft Delete Inspection
class DetailMedicationAuditView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicationAuditComprehensiveInspection.objects.filter(is_active=True)
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # If user is not authenticated, return empty queryset
        if not user.is_authenticated:
            return MedicationAuditComprehensiveInspection.objects.none()
        
        # Admin can see all inspections
        if user.role == 'admin' or user.role == 'team_leader' or user.role == 'inspector':
            return queryset
        
        # Worker can only see their own inspections
        elif user.role == 'worker':
            return queryset.filter(inspection__created_by=user)
        
        # Default: return empty queryset for other roles
        return MedicationAuditComprehensiveInspection.objects.none()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return InitiateMedicationAuditSerializer
        return MedicationAuditReadSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Medication Audit deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )