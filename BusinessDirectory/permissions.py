
from rest_framework import permissions

class IsVendorVerified(permissions.BasePermission):
    """
    Custom permission to check if the user is in the vendor table and is verified.
    Allows access if the user is authenticated and has a related vendor instance that is verified.
    """
    def has_permission(self, request, view):
        """
        Check if the user is authenticated and has a verified vendor profile.
        Args:
            request: Request instance.
            view: View instance.
        Returns:
            bool: True if the user is authenticated and has a verified vendor profile, False otherwise.
        """
        return request.user.is_authenticated and hasattr(request.user, 'vendor') and request.user.vendor.is_verified
        