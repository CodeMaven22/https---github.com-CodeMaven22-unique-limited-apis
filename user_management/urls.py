from django.urls import path
from .views import (
    InspectorListCreateView,
    InspectorDetailView,    
    AdminListCreateView,
    AdminDetailView,   
    WorkerListCreateView,
    WorkerDetailView,
    ClientListCreateView,
    ClientDetailView, 
)

urlpatterns = [
    path('inspectors/', InspectorListCreateView.as_view(), name='inspector-list-create'),
    path('inspectors/<int:pk>/', InspectorDetailView.as_view(), name='inspector-detail'),
    path('admins/', AdminListCreateView.as_view(), name='admin-list-create'),   
    path('admins/<int:pk>/', AdminDetailView.as_view(), name='admin-detail'),
    path('workers/', WorkerListCreateView.as_view(), name='worker-list-create'),
    path('workers/<int:pk>/', WorkerDetailView.as_view(), name='worker-detail'),
    path('clients/', ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
]