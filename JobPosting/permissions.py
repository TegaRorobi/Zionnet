
from rest_framework import permissions


class HasFreelancerProfile(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                hasattr(request.user, 'freelancer_profile')
            )
        )
