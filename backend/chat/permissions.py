from rest_framework import permissions

class IsChatSender(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.from_user == request.user
        