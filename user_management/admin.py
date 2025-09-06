from django.contrib import admin
from .models import Inspector, Admin as AdminModel, Worker, Client


@admin.register(Inspector)
class InspectorAdmin(admin.ModelAdmin):
    list_display = ('inspector', 'years_of_experience')
    search_fields = ('inspector__email', 'inspector__first_name', 'inspector__last_name')
    autocomplete_fields = ['inspector']


@admin.register(AdminModel)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('admin', 'office_location')
    search_fields = ('admin__email', 'admin__first_name', 'admin__last_name')
    autocomplete_fields = ['admin']


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('worker', 'department', 'shift_type', 'shift_time', 'hire_date')
    list_filter = ('department', 'shift_type')
    search_fields = ('worker__email', 'worker__first_name', 'worker__last_name')
    autocomplete_fields = ['worker']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client', 'age', 'company_name')
    search_fields = ('client__email', 'client__first_name', 'client__last_name')
    autocomplete_fields = ['client']
