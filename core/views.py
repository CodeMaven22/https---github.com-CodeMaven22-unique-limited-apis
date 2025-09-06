from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import calendar

from inspections.models.base import BaseInspection 

User = get_user_model()
from .serializers import (
    # UserLoginSerializer,
    UserWriteSerializer,
    UserReadSerializer, 
    UserUpdateSerializer, 
    PasswordChangeSerializer,
    CustomTokenObtainPairSerializer
)
from .models import User
from django.db.models import Q
from core.permissions import IsAdminOnly, IsAdminOrInspector


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    pagination_class = None  

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminOnly()]
        return [IsAdminOrInspector()]
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserWriteSerializer
        return UserReadSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)



class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    lookup_field = 'pk'

    def get_permissions(self):
        # DELETE → admin only
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminOnly()]
        
        # UPDATE → user can update themselves OR admin/inspector can update anyone
        elif self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated()]
        
        # VIEW → user can view themselves OR admin can view anyone
        elif self.request.method == 'GET':
            return [IsAuthenticated()]
        
        return [IsAuthenticated()]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserReadSerializer

    def get_object(self):
        obj = super().get_object()
        # Optional: Ensure non-admin users can only access themselves
        if not self.request.user.is_staff and obj != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only view or edit your own profile.")
        return obj 


# --- Custom Token View ---
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# class UserLoginView(APIView):
#     permission_classes = [AllowAny]  
    
#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             print("JWT Token:", serializer.validated_data.get('token'))
#             return Response(serializer.validated_data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserReadSerializer

    def get_object(self):
        return self.request.user


class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # ensures only current user can change their own password

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)



# DASHBOARD STATiSTICS 



class DashboardStatsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        # Total inspections count
        total_inspections = BaseInspection.objects.count()
        
        # Inspections by status
        status_counts = BaseInspection.objects.values('status').annotate(
            count=Count('id')
        )
        
        # Convert status counts to a more usable format
        status_data = {item['status']: item['count'] for item in status_counts}
        
        # Inspections by type
        type_counts = BaseInspection.objects.values('inspection_type').annotate(
            count=Count('id')
        )
        
        # User counts by role
        user_stats = User.objects.filter(is_active=True).values(
            'role'
        ).annotate(
            count=Count('id')
        )
        
        # Monthly trends (last 6 months)
        monthly_data = []
        for i in range(5, -1, -1):
            month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=30*i)
            month_end = month_start.replace(day=calendar.monthrange(month_start.year, month_start.month)[1])
            
            month_count = BaseInspection.objects.filter(
                created_at__gte=month_start,
                created_at__lte=month_end
            ).count()
            
            monthly_data.append({
                'month': month_start.strftime('%b %Y'),
                'count': month_count
            })
        
        # Detailed inspection type breakdown
        inspection_types = [
            'fire_alarm',
            'health_safety', 
            'medication_comprehensive',
            'smoke_alarm',
            'weekly_medication'
        ]
        
        type_breakdown = []
        for insp_type in inspection_types:
            count = BaseInspection.objects.filter(inspection_type=insp_type).count()
            type_breakdown.append({
                'type': insp_type,
                'count': count,
                'display_name': self.get_display_name(insp_type)
            })
        
        return Response({
            'total_inspections': total_inspections,
            'status_counts': status_data,
            'type_counts': list(type_counts),
            'type_breakdown': type_breakdown,
            'user_stats': list(user_stats),
            'monthly_trends': monthly_data,
            'pending_inspections': status_data.get('pending', 0),
            'approved_inspections': status_data.get('approved', 0),
            'rejected_inspections': status_data.get('rejected', 0),
            'completed_inspections': status_data.get('completed', 0),
        })
    
    def get_display_name(self, inspection_type):
        """Convert inspection type to readable format"""
        type_map = {
            'fire_alarm': 'Fire Alarm',
            'health_safety': 'Health & Safety',
            'medication_comprehensive': 'Medication Comprehensive',
            'smoke_alarm': 'Smoke Alarm',
            'weekly_medication': 'Weekly Medication'
        }
        return type_map.get(inspection_type, inspection_type.replace('_', ' ').title())


class InspectionTypeStatsView(generics.GenericAPIView):
    """Get detailed statistics for each inspection type"""
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        # Get counts for each specific inspection type with status breakdown
        inspection_types = [
            'fire_alarm',
            'health_safety', 
            'medication_comprehensive',
            'smoke_alarm',
            'weekly_medication'
        ]
        
        results = []
        for insp_type in inspection_types:
            # Get base inspections for this type
            base_inspections = BaseInspection.objects.filter(inspection_type=insp_type)
            total = base_inspections.count()
            
            # Get status breakdown
            status_breakdown = base_inspections.values('status').annotate(
                count=Count('id')
            )
            
            # Convert to dict format
            status_dict = {item['status']: item['count'] for item in status_breakdown}
            
            results.append({
                'type': insp_type,
                'display_name': self.get_display_name(insp_type),
                'total': total,
                'pending': status_dict.get('pending', 0),
                'approved': status_dict.get('approved', 0),
                'rejected': status_dict.get('rejected', 0),
                'completed': status_dict.get('completed', 0),
            })
        
        return Response(results)
    
    def get_display_name(self, inspection_type):
        """Convert inspection type to readable format"""
        type_map = {
            'fire_alarm': 'Fire Alarm',
            'health_safety': 'Health & Safety',
            'medication_comprehensive': 'Medication Comprehensive',
            'smoke_alarm': 'Smoke Alarm',
            'weekly_medication': 'Weekly Medication'
        }
        return type_map.get(inspection_type, inspection_type.replace('_', ' ').title())
# # SEARCH 
# class UserSearchView(generics.ListAPIView):
#     serializer_class = UserReadSerializer
#     permission_classes = [IsAdminOrInspector]

#     def get_queryset(self):
#         queryset = User.objects.all()
#         params = self.request.query_params

#         role = params.get('role', None)
#         name = params.get('name', None)
#         email = params.get('email', None)
#         location = params.get('location', None)

#         if role:
#             queryset = queryset.filter(role__iexact=role)

#         if name:
#             queryset = queryset.filter(
#                 Q(first_name__icontains=name) | Q(last_name__icontains=name)
#             )

#         if email:
#             queryset = queryset.filter(email__icontains=email)

#         if location:
#             queryset = queryset.filter(location__icontains=location)

#         return queryset

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     if not queryset.exists():
    #         return Response(
    #             {"detail": "No users found matching your criteria."},
    #             status=status.HTTP_404_NOT_FOUND
    #         )

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)





# class CombinedUserLoginView(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = CombinedUserLoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.validated_data, status=status.HTTP_200_OK)