from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    """Allows access only to superusers."""
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    

class IsParticipant(BasePermission):
    """Allows access to participants only."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not request.user.is_superuser