from rest_framework import generics, permissions, response, status
from inspections.models import HealthSafetyChecklist
from inspections.serializers.health_safety_checklist_serializers import (
    InitiateHealthSafetyChecklistSerializer,
    HealthSafetyChecklistReadSerializer
)
from core.permissions import IsWorkerOrInspector, IsAdminOnly, IsInspectorOrAdmin


class ListCreateHealthSafetyChecklistView(generics.ListCreateAPIView):
    queryset = HealthSafetyChecklist.objects.filter(is_active=True)
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # If user is not authenticated, return empty queryset
        if not user.is_authenticated:
            return HealthSafetyChecklist.objects.none()
        
        # Admin can see all inspections
        if user.role == 'admin' or user.role == 'team_leader' or user.role == 'inspector':
            return queryset
        
        # Worker can only see their own inspections
        elif user.role == 'worker':
            return queryset.filter(inspection__created_by=user)
        
        # Default: return empty queryset for other roles
        return FireAlarmWeeklyInspection.objects.none()
   
    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return InitiateHealthSafetyChecklistSerializer
        return HealthSafetyChecklistReadSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

class DetailHealthSafetyChecklistView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HealthSafetyChecklist.objects.filter(is_active=True)
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # If user is not authenticated, return empty queryset
        if not user.is_authenticated:
            return HealthSafetyChecklist.objects.none()
        
        # Admin can see all inspections
        if user.role == 'admin' or user.role == 'team_leader' or user.role == 'inspector':
            return queryset
        
        # Worker can only see their own inspections
        elif user.role == 'worker':
            return queryset.filter(inspection__created_by=user)
        
        # Default: return empty queryset for other roles
        return HealthSafetyChecklist.objects.none()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return InitiateHealthSafetyChecklistSerializer
        return HealthSafetyChecklistReadSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), IsAdminOnly()]
        return [permissions.AllowAny()]

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(
            {"detail": "Health Safety Checklist deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        ) 
    

# class HealthSafetyChecklistListView(generics.ListAPIView):
#     queryset = HealthSafetyChecklist.objects.all()
#     serializer_class = HealthSafetyChecklistReadSerializer

#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [permissions.AllowAny()]
#         return [permissions.IsAuthenticated()]


# class HealthSafetyChecklistDetailView(generics.RetrieveAPIView):
#     queryset = HealthSafetyChecklist.objects.all()
#     serializer_class = HealthSafetyChecklistReadSerializer
#     permission_classes = [permissions.IsAuthenticated]
