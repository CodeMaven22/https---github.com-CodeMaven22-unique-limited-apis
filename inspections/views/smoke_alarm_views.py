from rest_framework import generics, status, permissions
from rest_framework.response import Response
from inspections.models.smoke_alarm_weekly import SmokeAlarmWeeklyInspection
from inspections.serializers.smoke_alarm_serializers import (
    SmokeAlarmWeeklySerializer, 
    SmokeAlarmWeeklyInspectionReadSerializer
)
from core.permissions import IsWorkerOrInspector, IsInspectorOrAdmin, IsAdminOnly

# 1. Initiate or List Inspections (Workers or Inspectors)
class ListCreateSmokeAlarmWeeklyInspectionView(generics.ListCreateAPIView):
    queryset = SmokeAlarmWeeklyInspection.objects.filter(is_active=True)
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # If user is not authenticated, return empty queryset
        if not user.is_authenticated:
            return SmokeAlarmWeeklyInspection.objects.none()
        
        # Admin can see all inspections
        if user.role == 'admin' or user.role == 'team_leader' or user.role == 'inspector':
            return queryset
        
        # Worker can only see their own inspections
        elif user.role == 'worker':
            return queryset.filter(inspection__created_by=user)
        
        # Default: return empty queryset for other roles
        return SmokeAlarmWeeklyInspection.objects.none()


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SmokeAlarmWeeklySerializer
        return SmokeAlarmWeeklyInspectionReadSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

# 4. Retrieve / Update / Soft Delete Inspection
class DetailSmokeAlarmWeeklyInspectionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SmokeAlarmWeeklySerializer.Meta.model.objects.filter(is_active=True)
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # If user is not authenticated, return empty queryset
        if not user.is_authenticated:
            return SmokeAlarmWeeklyInspection.objects.none()
        
        # Admin can see all inspections
        if user.role == 'admin' or user.role == 'team_leader' or user.role == 'inspector':
            return queryset
        
        # Worker can only see their own inspections
        elif user.role == 'worker':
            return queryset.filter(inspection__created_by=user)
        
        # Default: return empty queryset for other roles
        return SmokeAlarmWeeklyInspection.objects.none()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SmokeAlarmWeeklySerializer
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), IsAdminOnly()]
        return SmokeAlarmWeeklyInspectionReadSerializer

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