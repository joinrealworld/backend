from rest_framework import permissions

class IsLoggedInUserOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_admin

class IsLoggedInUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user