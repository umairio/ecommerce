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
    list_display = ("__str__", "product", "rating", "comment")


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "price",
        "category",
        "seller",
        "shop",
        "rating",
    )
    list_filter = ("category", "seller", "shop")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "buyer",
        "seller",
        "product",
        "shop",
        "quantity",
        "total_amount",
        "status",
        "review_rating",
    )

    def review_rating(self, obj):
        return obj.review.rating


class ShopAdmin(admin.ModelAdmin):
    list_display = ("owner", "name", "rating")


class InventoryAdmin(admin.ModelAdmin):
    list_display = ("product", "shop", "seller", "total_quantity")
    list_filter = ("shop", "seller", "product__category")


admin.site.register(Profile, ProfileAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Inventory, InventoryAdmin)
