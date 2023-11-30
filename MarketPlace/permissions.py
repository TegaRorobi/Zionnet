from rest_framework import permissions
from .models import Store


class IsStoreOwner(permissions.BasePermission):
    """
    Custom permission to check if the user is Authenticated
    Allows access if the user is authenticated and is the owner of the store.
    """

    def has_permission(self, request, view):
        store_id = view.kwargs["id"]

        if store_id:
            store_owner = Store.objects.filter(id=store_id).values("vendor").first()
            return (
                request.user.is_authenticated
                and hasattr(request.user, "stores")
                and request.user == store_owner["vendor"]
            )
        return False
