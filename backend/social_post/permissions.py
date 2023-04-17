from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object level permission to only allow PUT, PATCH, DELETE for owner only and read only for others
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user 
