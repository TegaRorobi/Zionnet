from rest_framework import permissions

class IsOrderOwner(permissions.BasePermission):
    """
    Custom permission to only allow the owner of an order to view, update, or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the owner of the order
        return obj.buyer == request.user
