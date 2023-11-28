
from rest_framework import permissions

class IsVendorVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'vendor') and request.user.vendor.is_verified
        