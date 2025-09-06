# 2. Conduct Inspection (Inspector or Admin)
from core.permissions import IsInspectorOrAdmin,  IsAdminOnly
from inspections.models.base import BaseInspection
from inspections.serializers.base_serializers import ConductInspectionSerializer, ApproveInspectionSerializer
from rest_framework import generics, permissions


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from  ..models.base import BaseInspection
from ..serializers import BaseInspectionSerializer
from datetime import datetime


class InspectionSearchView(generics.ListAPIView):
    serializer_class = BaseInspectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = BaseInspection.objects.all()
        params = self.request.query_params

        inspection_type = params.get('inspection_type', None)
        status_param = params.get('status', None)
        client_name = params.get('client_name', None)
        location = params.get('location', None)
        start_date = params.get('start_date', None)
        end_date = params.get('end_date', None)

        # Enum-like fields: iexact
        if inspection_type:
            queryset = queryset.filter(inspection_type__iexact=inspection_type)
        if status_param:
            queryset = queryset.filter(status__iexact=status_param)

        # Free-text fields: icontains
        if client_name:
            queryset = queryset.filter(client_name__icontains=client_name)
        if location:
            queryset = queryset.filter(location__icontains=location)

        # Date range filter
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"detail": "No inspections found matching your criteria."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ConductInspectionView(generics.UpdateAPIView):
    queryset = BaseInspection.objects.all()
    serializer_class = ConductInspectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsInspectorOrAdmin]
    lookup_field = 'pk'

    def get_serializer_context(self):
        return {'request': self.request}


# 3. Approve Inspection (Admin Only)
class ApproveInspectionView(generics.UpdateAPIView):
    queryset = BaseInspection.objects.all()
    serializer_class = ApproveInspectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOnly]
    lookup_field = 'pk'

    def get_serializer_context(self):
        return {'request': self.request}