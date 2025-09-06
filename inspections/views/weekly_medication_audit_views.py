from rest_framework import generics, status, permissions
from rest_framework.response import Response
from inspections.models.weekly_medication_audit import WeeklyMedicationAuditInspection
from inspections.serializers.weekly_medication_audit_serializers import (
    WeeklyMedicationAuditSerializer,
    WeeklyMedicationAuditReadSerializer
)
from core.permissions import IsAdminOnly, IsWorkerOrInspector

class ListCreateWeeklyMedicationAuditView(generics.ListCreateAPIView):
    queryset = WeeklyMedicationAuditInspection.objects.all()
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # If user is not authenticated, return empty queryset
        if not user.is_authenticated:
            return WeeklyMedicationAuditInspection.objects.none()
        
        # Admin can see all inspections
        if user.role == 'admin' or user.role == 'team_leader' or user.role == 'inspector':
            return queryset
        
        # Worker can only see their own inspections
        elif user.role == 'worker':
            return queryset.filter(inspection__created_by=user)
        
        # Default: return empty queryset for other roles
        return WeeklyMedicationAuditInspection.objects.none()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WeeklyMedicationAuditSerializer
        return WeeklyMedicationAuditReadSerializer
    

    def get_serializer_context(self):
        return {'request': self.request}
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class DetailWeeklyMedicationAuditView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WeeklyMedicationAuditInspection.objects.filter(is_active=True)
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # If user is not authenticated, return empty queryset
        if not user.is_authenticated:
            return WeeklyMedicationAuditInspection.objects.none()
        
        # Admin can see all inspections
        if user.role == 'admin' or user.role == 'team_leader' or user.role == 'inspector':
            return queryset
        
        # Worker can only see their own inspections
        elif user.role == 'worker':
            return queryset.filter(inspection__created_by=user)
        
        # Default: return empty queryset for other roles
        return WeeklyMedicationAuditInspection.objects.none()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return WeeklyMedicationAuditSerializer
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated()]
        return WeeklyMedicationAuditReadSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Inspection deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )