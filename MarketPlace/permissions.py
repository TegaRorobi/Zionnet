from rest_framework import permissions
from .models import Store


class IsStoreOwner(permissions.BasePermission):
    """
    Custom permission to check if the user is Authenticated
    Allows access if the user is authenticated and is the owner of the store.
    """

    def has_permission(self, request, view):
        store_id = view.kwargs["store_id"]

        if store_id:
            store_owner = (
                Store.objects.filter(id=store_id)
                .values_list("vendor", flat=True)
                .first()
            )
            return request.user.is_authenticated and request.user.id == store_owner
        return False


class IsOrderOwner(permissions.BasePermission):
    """
    Custom permission to only allow the owner of an order to view, update, or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the owner of the order
        return obj.buyer == request.user
