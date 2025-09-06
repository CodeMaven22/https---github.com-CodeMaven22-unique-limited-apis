from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    # UserLoginView,
    UserListCreateView,
    UserDetailView,
    PasswordChangeView,
    ProfileView,
    DashboardStatsView,
    InspectionTypeStatsView
    
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # JWT token endpoints
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # path('login/', UserLoginView.as_view(), name='combined-login'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    # me 
    path("user/profile/", ProfileView.as_view(), name="profile"),
    path("user/change-password/", PasswordChangeView.as_view(), name="change-password"),

     path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('dashboard/inspection-types/', InspectionTypeStatsView.as_view(), name='inspection-type-stats'),
]
