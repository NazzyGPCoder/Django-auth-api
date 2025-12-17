from rest_framework.permissions import BasePermission, SAFE_METHODS
from role.models import UserRole


class IsAdminOrSuperAdmin(BasePermission):
    """
    Only Admin and Super Admin can create, update, delete
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]
        ) 


class IsReadOnlyOrAdmin(BasePermission):
    """
    Anyone can read, only Admin / Super Admin can write
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated and
            request.user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]
        )
