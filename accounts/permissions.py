from rest_framework.permissions import BasePermission

from .models import User


class IsAdminRole(BasePermission):

    message = "Admin access required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.ADMIN
        )