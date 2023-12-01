
from rest_framework import permissions

class IsApprovedStoreVendor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                hasattr(request.user, 'store_vendor_profile') and (
                    request.user.store_vendor_profile.is_approved
                )
            )
        )
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.store_vendor_profile == obj.vendor
        )

class IsOrderOwner(permissions.BasePermission):
    """
    Custom permission to only allow the owner of an order to view, update, or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the owner of the order
        return obj.buyer == request.user
