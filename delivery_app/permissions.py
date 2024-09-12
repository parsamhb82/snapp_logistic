from .models import Courier
from rest_framework.permissions import BasePermission


class CourierPermission(BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'courier'):
            return True
        return False
    
    
class SuperUserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return True
        return False

