from rest_framework import permissions

from .constants import ProfileRole


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.user.profile.role == ProfileRole.OWNER
            or request.user.profile.role == ProfileRole.ADMIN
        ):
            return True
        return False


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.is_authenticated
            and request.user.profile.role != ProfileRole.BUYER
        ):
            return True
        return False


class IsBuyer(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.is_authenticated
            and request.user.profile.role == ProfileRole.BUYER
        ):
            return True
        return False
