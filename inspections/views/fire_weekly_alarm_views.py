from rest_framework import generics, permissions, status
from rest_framework.response import Response
# inspections/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models import Q
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from io import BytesIO
import pandas as pd
import json
from datetime import datetime, timedelta
import csv

from inspections.models import FireAlarmWeeklyInspection, BaseInspection
from inspections.serializers import FireAlarmWeeklyInspectionReadSerializer
from ..models import BaseInspection, FireAlarmWeeklyInspection
from ..serializers import (
    InitiateFireAlarmWeeklySerializer,
    FireAlarmWeeklyInspectionReadSerializer
)
from core.permissions import IsWorkerOrInspector , IsAdminOnly, IsAdminOrInspector


# 1. Initiate or List Inspections (Workers or Inspectors)
class ListCreateInspectionView(generics.ListCreateAPIView):
    queryset = FireAlarmWeeklyInspection.objects.filter(is_active=True)
    pagination_class = None
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # If user is not authenticated, return empty queryset
        if not user.is_authenticated:
            return FireAlarmWeeklyInspection.objects.none()
        
        # Admin can see all inspections
        if user.role == 'admin' or user.role == 'team_leader' or user.role == 'inspector':
            return queryset
        
        # Worker can only see their own inspections
        elif user.role == 'worker':
            return queryset.filter(inspection__created_by=user)
        
        # Default: return empty queryset for other roles
        return FireAlarmWeeklyInspection.objects.none()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return InitiateFireAlarmWeeklySerializer
        return FireAlarmWeeklyInspectionReadSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
# class ListCreateInspectionView(generics.ListCreateAPIView):
#     queryset = FireAlarmWeeklyInspection.objects.filter(is_active=True)
#     pagination_class = None
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return InitiateFireAlarmWeeklySerializer
#         return FireAlarmWeeklyInspectionReadSerializer

#     def get_serializer_context(self):
#         return {'request': self.request}

#     def get_permissions(self):
#         if self.request.method == 'POST':
#             return [permissions.IsAuthenticated()]
#         return [permissions.AllowAny()]

class DetailFireAlarmWeeklyInspectionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FireAlarmWeeklyInspection.objects.filter(is_active=True)
    lookup_field = 'pk'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # If user is not authenticated, return empty queryset
        if not user.is_authenticated:
            return FireAlarmWeeklyInspection.objects.none()
        
        # Admin can see all inspections
        if user.role == 'admin' or user.role == 'team_leader' or user.role == 'inspector':
            return queryset
        
        # Worker can only see their own inspections
        elif user.role == 'worker':
            return queryset.filter(inspection__created_by=user)
        
        # Default: return empty queryset for other roles
        return FireAlarmWeeklyInspection.objects.none()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return InitiateFireAlarmWeeklySerializer
        return FireAlarmWeeklyInspectionReadSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), IsAdminOnly()]
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

# 4. Retrieve / Update / Soft Delete Inspection
# class DetailFireAlarmWeeklyInspectionView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = FireAlarmWeeklyInspection.objects.filter(is_active=True)
#     lookup_field = 'pk'

#     def get_serializer_class(self):
#         if self.request.method in ['PUT', 'PATCH']:
#             return InitiateFireAlarmWeeklySerializer
#         return FireAlarmWeeklyInspectionReadSerializer

#     def get_serializer_context(self):
#         return {'request': self.request}

#     def get_permissions(self):
#         if self.request.method in ['PUT', 'PATCH']:
#             return [permissions.IsAuthenticated()]
#         elif self.request.method == 'DELETE':
#             return [permissions.IsAuthenticated(), IsAdminOnly()]
#         return [permissions.AllowAny()]

#     def perform_destroy(self, instance):
#         instance.is_active = False
#         instance.save()

#     def delete(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(
#             {"detail": "Inspection deleted successfully."},
#             status=status.HTTP_204_NO_CONTENT
#         )







class FireAlarmReportView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        format_type = request.GET.get('format', 'pdf')
        status = request.GET.get('status', 'all')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        # Build query filters
        filters = Q()
        
        if status != 'all':
            filters &= Q(inspection__status=status)
        
        if date_from and date_to:
            try:
                from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
                to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
                filters &= Q(inspection__created_at__date__gte=from_date)
                filters &= Q(inspection__created_at__date__lte=to_date)
            except ValueError:
                return Response({"error": "Invalid date format"}, status=400)
        
        # Filter inspections
        inspections = FireAlarmWeeklyInspection.objects.filter(
            filters, 
            is_active=True
        ).select_related('inspection')
        
        if format_type == 'pdf':
            return self.generate_pdf_report(inspections, request)
        elif format_type == 'excel':
            return self.generate_excel_report(inspections)
        elif format_type == 'json':
            return self.generate_json_report(inspections)
        elif format_type == 'csv':
            return self.generate_csv_report(inspections)
        else:
            return Response({"error": "Unsupported format"}, status=400)
    
    def generate_pdf_report(self, inspections, request):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center
        )
        
        # Title
        title = Paragraph("Fire Alarm Inspection Report", title_style)
        elements.append(title)
        
        # Report metadata
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Paragraph(f"Total inspections: {inspections.count()}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Inspection data table
        if inspections.exists():
            # Table data
            table_data = [['ID', 'Client', 'Location', 'Status', 'Date', 'Point Checked', 'Alarm Functional']]
            
            for inspection in inspections:
                table_data.append([
                    str(inspection.id),
                    inspection.inspection.client_name or 'N/A',
                    inspection.inspection.location or 'N/A',
                    inspection.inspection.status,
                    inspection.inspection.created_at.strftime('%Y-%m-%d'),
                    inspection.point_checked or 'N/A',
                    'Yes' if inspection.alarm_functional else 'No'
                ])
            
            # Create table
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
        else:
            elements.append(Paragraph("No inspections found for the selected criteria.", styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="fire-alarm-inspection-report.pdf"'
        return response
    
    def generate_excel_report(self, inspections):
        # Prepare data
        data = []
        for inspection in inspections:
            data.append({
                'ID': inspection.id,
                'Client Name': inspection.inspection.client_name,
                'Location': inspection.inspection.location,
                'Status': inspection.inspection.status,
                'Inspection Date': inspection.inspection.created_at.date(),
                'Point Checked': inspection.point_checked,
                'Alarm Functional': 'Yes' if inspection.alarm_functional else 'No',
                'Call Points Accessible': 'Yes' if inspection.call_points_accessible else 'No',
                'Emergency Lights Working': 'Yes' if inspection.emergency_lights_working else 'No',
                'Faults Identified': inspection.faults_identified_details,
                'Action Taken': inspection.action_taken_details,
                'Management Book Initials': inspection.management_book_initials,
                'Comments': inspection.comments,
                'Created By': inspection.inspection.created_by.get_full_name() if inspection.inspection.created_by else 'N/A'
            })
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Create Excel file
        excel_file = BytesIO()
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Fire Alarm Inspections', index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets['Fire Alarm Inspections']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        excel_file.seek(0)
        
        response = HttpResponse(excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="fire-alarm-inspection-report.xlsx"'
        return response
    
    def generate_json_report(self, inspections):
        # Use serializer to get consistent data format
        serializer = FireAlarmWeeklyInspectionReadSerializer(inspections, many=True)
        data = serializer.data
        
        response = HttpResponse(
            json.dumps(data, indent=2, default=str), 
            content_type='application/json'
        )
        response['Content-Disposition'] = 'attachment; filename="fire-alarm-inspection-report.json"'
        return response
    
    def generate_csv_report(self, inspections):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="fire-alarm-inspection-report.csv"'
        
        writer = csv.writer(response)
        # Write header
        writer.writerow([
            'ID', 'Client Name', 'Location', 'Status', 'Inspection Date',
            'Point Checked', 'Alarm Functional', 'Call Points Accessible',
            'Emergency Lights Working', 'Faults Identified', 'Action Taken',
            'Management Book Initials', 'Comments', 'Created By'
        ])
        
        # Write data
        for inspection in inspections:
            writer.writerow([
                inspection.id,
                inspection.inspection.client_name or '',
                inspection.inspection.location or '',
                inspection.inspection.status,
                inspection.inspection.created_at.date(),
                inspection.point_checked or '',
                'Yes' if inspection.alarm_functional else 'No',
                'Yes' if inspection.call_points_accessible else 'No',
                'Yes' if inspection.emergency_lights_working else 'No',
                inspection.faults_identified_details or '',
                inspection.action_taken_details or '',
                inspection.management_book_initials or '',
                inspection.comments or '',
                inspection.inspection.created_by.get_full_name() if inspection.inspection.created_by else ''
            ])
        
        return response


class QuickFireAlarmReportView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, report_type):
        if report_type == 'summary':
            return self.generate_summary_report(request)
        elif report_type == 'detailed':
            return self.generate_detailed_report(request)
        elif report_type == 'analytics':
            return self.generate_analytics_report(request)
        else:
            return Response({"error": "Unknown report type"}, status=400)
    
    def generate_summary_report(self, request):
        # Last 30 days summary
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        inspections = FireAlarmWeeklyInspection.objects.filter(
            inspection__created_at__gte=thirty_days_ago,
            is_active=True
        ).select_related('inspection')
        
        return self.generate_pdf_report(inspections, request, "30-Day Summary Report")
    
    def generate_detailed_report(self, request):
        # All inspections with details
        inspections = FireAlarmWeeklyInspection.objects.filter(
            is_active=True
        ).select_related('inspection')
        
        return self.generate_excel_report(inspections, "Detailed Inspection Report")
    
    def generate_analytics_report(self, request):
        # Analytics with charts and stats
        inspections = FireAlarmWeeklyInspection.objects.filter(
            is_active=True
        ).select_related('inspection')
        
        # This would be more complex with actual analytics
        return self.generate_pdf_report(inspections, request, "Analytics Report")
    
    def generate_pdf_report(self, inspections, request, title):
        # Similar to previous PDF generation but with different title
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1
        )
        
        elements.append(Paragraph(title, title_style))
        # ... rest of PDF generation code
        
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{title.lower().replace(" ", "-")}.pdf"'
        return response
    
    def generate_excel_report(self, inspections, title):
        # Similar to previous Excel generation
        # ... Excel generation code
        pass