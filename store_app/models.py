from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _

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
    class Role(models.TextChoices):
        Admin = "admin"
        Owner = "owner"
        Buyer = "buyer"
        Seller = "seller"

    user = models.OneToOneField(
        "User", verbose_name=_("user"), on_delete=models.CASCADE
    )
    profile_pic = models.ImageField(
        _("profile picture"), upload_to="profile_pics", blank=True
    )
    role = models.CharField(
        _("role"), max_length=10, choices=Role.choices, default=Role.Buyer
    )
    phone_number = models.CharField(_("phone number"), max_length=15)

    def __str__(self):
        return self.user.email


class Category(models.Model):
    name = models.CharField(_("name"), max_length=50)

    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        Null = "null"
        Cart = "cart"
        Confirmed = "confirmed"
        Shipped = "shipped"
        Delivered = "delivered"

    buyer = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="buyer"
    )
    seller = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="seller"
    )
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="order"
    )
    shop = models.ForeignKey(
        "Shop", on_delete=models.CASCADE, related_name="order"
    )
    quantity = models.IntegerField(_("quantity"))
    total_amount = models.IntegerField(_("total amount"))
    shipping_address = models.TextField(_("shipping address"))
    status = models.CharField(
        _("status"), max_length=10, choices=Status.choices, default=Status.Null
    )

    def __str__(self):
        return self.buyer.user.email


class Inventory(models.Model):
    shop = models.ForeignKey(
        "Shop", on_delete=models.CASCADE, related_name="inventory"
    )
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="inventory"
    )
    seller = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="inventory"
    )
    total_quantity = models.IntegerField(_("total quantity"))

    def __str__(self):
        return self.product.name


class Review(models.Model):
    reviewer = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="review"
    )
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="review"
    )
    order = models.OneToOneField(
        "Order", on_delete=models.CASCADE, related_name="review", null=True
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
        "Category", on_delete=models.CASCADE, related_name="product"
    )
    seller = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="product"
    )
    shop = models.ForeignKey(
        "Shop", on_delete=models.CASCADE, related_name="product"
    )

    @property
    def rating(self):
        average_rating = self.review.aggregate(Avg("rating"))["rating__avg"]
        return round(average_rating, 2) if average_rating is not None else None

    def __str__(self):
        return self.name


class Shop(models.Model):
    owner = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="shop"
    )
    name = models.CharField(_("name"), max_length=50)

    @property
    def rating(self):
        average_rating = self.product.aggregate(Avg("review__rating"))[
            "review__rating__avg"
        ]
        return round(average_rating, 2) if average_rating is not None else None

    def __str__(self):
        return self.name
