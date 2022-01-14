from rest_framework import permissions

from accounts.models import User


class IsEventOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user in [obj.client, obj.expert]
