from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _

from .constants import OrderStatus, ProfileRole
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_superuser = models.BooleanField(_("superuser status"), default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


class Profile(models.Model):
    user = models.OneToOneField(
        "User", verbose_name=_("user"), on_delete=models.CASCADE
    )
    profile_pic = models.ImageField(
        _("profile picture"), upload_to="profile_pics", blank=True
    )
    role = models.CharField(
        _("role"),
        max_length=10,
        choices=ProfileRole.ROLE,
        default=ProfileRole.BUYER,
    )
    phone_number = models.CharField(_("phone number"), max_length=15)

    def __str__(self):
        return self.user.email


class Category(models.Model):
    name = models.CharField(_("name"), max_length=50)

    def __str__(self):
        return self.name


class Order(models.Model):

    buyer = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="order_buyer"
    )
    seller = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="order_seller"
    )
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="order_product"
    )
    shop = models.ForeignKey(
        "Shop", on_delete=models.CASCADE, related_name="order_shop"
    )
    quantity = models.IntegerField(_("quantity"))
    total_amount = models.IntegerField(_("total amount"))
    shipping_address = models.TextField(_("shipping address"))
    status = models.CharField(
        _("status"),
        max_length=10,
        choices=OrderStatus.STATUS,
        default=OrderStatus.CART,
    )

    def __str__(self):
        return self.buyer.user.email


class Inventory(models.Model):
    shop = models.ForeignKey(
        "Shop", on_delete=models.CASCADE, related_name="inventory_shop"
    )
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="inventory_product"
    )
    seller = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="inventory_seller"
    )
    total_quantity = models.IntegerField(_("total quantity"))

    def __str__(self):
        return self.product.name


class Review(models.Model):
    reviewer = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="reviewer"
    )
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="reviewed_product"
    )
    order = models.OneToOneField(
        "Order",
        on_delete=models.CASCADE,
        related_name="reviewed_order",
        null=True,
    )
    rating = models.IntegerField(_("rating"))
    comment = models.TextField(_("comment"))

    def __str__(self):
        return self.reviewer.user.email


class Product(models.Model):
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"))
    price = models.IntegerField(_("price"))
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="product_category"
    )
    seller = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="product_seller"
    )
    shop = models.ForeignKey(
        "Shop", on_delete=models.CASCADE, related_name="product_shop"
    )

    @property
    def rating(self):
        average_rating = self.reviewed_product.aggregate(Avg("rating"))[
            "rating__avg"
        ]
        return round(average_rating, 2) if average_rating else average_rating

    def __str__(self):
        return self.name


class Shop(models.Model):
    owner = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="owned_shops"
    )
    name = models.CharField(_("name"), max_length=50)

    @property
    def rating(self):
        average_rating = self.product_shop.aggregate(
            Avg("reviewed_product__rating")
        )["reviewed_product__rating__avg"]
        return round(average_rating, 2) if average_rating else average_rating

    def __str__(self):
        return self.name
