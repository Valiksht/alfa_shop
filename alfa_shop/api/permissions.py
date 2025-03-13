from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Является ли пользователь авторизованным."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                # or request.user.is_admin
                )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser
                # or request.user.is_admin
                )
