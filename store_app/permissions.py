from rest_framework import permissions

from .models import (
    Category,
    Inventory,
    Order,
    Product,
    Profile,
    Review,
    Shop,
    User,
)


class OwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.profile.role == Profile.Role.Owner
            or request.user.profile.role == Profile.Role.Admin
        ):
            return True
        return False

class SellerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.profile.role == Profile.Role.Owner
            or request.user.profile.role == Profile.Role.Admin
            or request.user.profile.role == Profile.Role.Seller
        ):
            return True
        return False