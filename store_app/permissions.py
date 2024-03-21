from rest_framework import permissions

from .constants import ProfileRole
from .models import Profile


class OwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.profile.role == ProfileRole.OWNER
            or request.user.profile.role == ProfileRole.ADMIN
        ):
            return True
        return False


class SellerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.profile.role != Profile.Role.BUYER:
            return True
        return False
