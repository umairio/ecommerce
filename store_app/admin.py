from django.contrib import admin

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


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("__str__", "role", "phone_number")


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "rating", "comment")


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "price",
        "category",
        "seller",
        "shop",
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "buyer",
        "seller",
        "shop",
        "quantity",
        "total_amount",
        "shipping_address",
    )


class ShopAdmin(admin.ModelAdmin):
    list_display = ("owner", "name", "rating")


class InventoryAdmin(admin.ModelAdmin):
    list_display = ("shop", "product", "seller", "total_quantity")


admin.site.register(Profile, ProfileAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Inventory, InventoryAdmin)
