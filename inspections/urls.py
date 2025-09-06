from django.urls import path
from inspections.views.fire_weekly_alarm_views import (
    ListCreateInspectionView,
    DetailFireAlarmWeeklyInspectionView,
    FireAlarmReportView,
    QuickFireAlarmReportView 
)
from inspections.views.base_view import (
    ConductInspectionView, 
    ApproveInspectionView,
    InspectionSearchView
)

from inspections.views.first_aid_checklist_views import (   
    ListCreateFirstAidChecklistInspectionView,
    DetailFirstAidChecklistView
)

from inspections.views.health_safety_checklist_views import (
    ListCreateHealthSafetyChecklistView,
    DetailHealthSafetyChecklistView
)


from inspections.views.medication_comprehensive_views import (
    ListCreateMedicationAuditView,
    DetailMedicationAuditView
)


from inspections.views.smoke_alarm_views import (   
    ListCreateSmokeAlarmWeeklyInspectionView,
    DetailSmokeAlarmWeeklyInspectionView
)


from inspections.views.weekly_medication_audit_views import (
    ListCreateWeeklyMedicationAuditView,
    DetailWeeklyMedicationAuditView
)

urlpatterns = [
    # Base Inspection Views
    path('base/conduct/<int:pk>/', ConductInspectionView.as_view(), name='conduct-inspection'),
    path('base/approve/<int:pk>/', ApproveInspectionView.as_view(), name='approve-inspection'),
    path('base/search/', InspectionSearchView.as_view(), name='search-inspections'),

    # Fire Alarm Weekly Inspections
    path('fire-alarm/', ListCreateInspectionView.as_view(), name='fire-alarm-list-create'),
    path('fire-alarm/<int:pk>/', DetailFireAlarmWeeklyInspectionView.as_view(), name='fire-alarm-detail'),
    path('fire-alarm/reports/', FireAlarmReportView.as_view(), name='fire-alarm-reports'),
    path('fire-alarm/reports/quick/<str:report_type>/', QuickFireAlarmReportView.as_view(), name='quick-fire-alarm-reports'),
    
    # First Aid Checklist Inspections
    path('first-aid/', ListCreateFirstAidChecklistInspectionView.as_view (), name='first-aid-list-create'),
    path('first-aid/<int:pk>/', DetailFirstAidChecklistView.as_view(), name='first-aid-detail'),

    # Health & Safety Checklist Inspections
    path('health-safety/', ListCreateHealthSafetyChecklistView.as_view(), name='health-safety-list-create'),
    path('health-safety/<int:pk>/', DetailHealthSafetyChecklistView.as_view(), name='health-safety-detail'),

    # Medication Audit Comprehensive Views
    path('medication-comprehensive/', ListCreateMedicationAuditView.as_view(), name='medication-comprehensive-list-create'),
    path('medication-comprehensive/<int:pk>/', DetailMedicationAuditView.as_view(), name='medication-comprehensive-detail'),
    
    # Smoke Alarm Weekly Inspections
    path('smoke-alarm/', ListCreateSmokeAlarmWeeklyInspectionView.as_view(), name='smoke-alarm-list-create'),
    path('smoke-alarm/<int:pk>/', DetailSmokeAlarmWeeklyInspectionView.as_view(), name='smoke-alarm-detail'),

    # Weekly Medication Audit Inspections
    path('weekly-medication-audit/', ListCreateWeeklyMedicationAuditView.as_view(), name='weekly-medication-audit-list-create'),
    path('weekly-medication-audit/<int:pk>/', DetailWeeklyMedicationAuditView.as_view(), name='weekly-medication-audit-detail'),
]
