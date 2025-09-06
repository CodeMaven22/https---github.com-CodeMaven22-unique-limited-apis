from rest_framework import generics, permissions, status
from rest_framework.response import Response

from rest_framework import generics, permissions
from inspections.models import FirstAidChecklistInspection
from inspections.serializers.first_aid_checklist_serializers import (
    InitiateFirstAidChecklistSerializer,
    FirstAidCheckListReadSerializer
)

from core.permissions import IsWorkerOrInspector, IsAdminOnly, IsInspectorOrAdmin


class ListCreateFirstAidChecklistInspectionView(generics.ListCreateAPIView):
    queryset = FirstAidChecklistInspection.objects.all()
    pagination_class =None

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return InitiateFirstAidChecklistSerializer
        return FirstAidCheckListReadSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsWorkerOrInspector()]
        return [permissions.AllowAny()]
    

class DetailFirstAidChecklistView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FirstAidChecklistInspection.objects.filter(is_active=True)
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return InitiateFirstAidChecklistSerializer
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), IsAdminOnly()]
        return FirstAidCheckListReadSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated(), IsInspectorOrAdmin()]
        return [permissions.AllowAny()]
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "First Aid Checklist Inspection deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )