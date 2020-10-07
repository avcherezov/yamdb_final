from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        role = getattr(request.user, 'role', '')
        if role in ['admin'] or request.user.is_superuser:
            return True
        return False


class IsUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'PATCH']:
            return obj == request.user
        return False


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return getattr(request.user, 'role', '') == 'moderator'

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class UserRolePermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'DELETE' and user.role == 'moderator':
            return True
        return user == obj.author


class IsAdminOrReadOnlyPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        role = getattr(request.user, 'role', '')
        if (role in ['admin'] or request.user.is_superuser or
                (request.method in SAFE_METHODS)):
            return True
        return False


class IsAdminOrReadOnlyPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(request.user.is_superuser or
                request.user.role == 'admin')
        return False
