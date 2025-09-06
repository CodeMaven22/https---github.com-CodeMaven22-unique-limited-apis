from rest_framework.permissions import BasePermission

class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role== 'admin'


class IsInspectorOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'inspector'


class IsWorkerOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'worker'

class IsWorkerOrInspector(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and  request.user.role in ['worker', 'inspector']
    
class IsAdminOrInspector(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin' or request.user.role == 'inspector'

class IsInspectorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['inspector', 'admin']
from rest_framework import permissions









