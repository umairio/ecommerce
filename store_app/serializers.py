from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .constants import OrderStatus, ProfileRole
from .models import Inventory, Order, Product, Profile, Review, Shop, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ["id", "user", "profile_pic", "role", "phone_number"]


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, attrs):
        if attrs["rating"] > 5 or attrs["rating"] < 1:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return attrs

    def validate_order(self, value):
        if value.status != OrderStatus.DELIVERED:
            raise serializers.ValidationError(
                "Order must be in delivered first"
            )
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate(self, attrs):
        if attrs["price"] < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"

    def validate(self, attrs):
        owner = attrs.get("owner")
        if owner.profile.role != ProfileRole.Owner:
            raise serializers.ValidationError(f"{owner} is not an owner")
        return attrs


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"

    def validate(self, attrs):
        seller = attrs.get("seller")
        if seller.profile.role != ProfileRole.Seller:
            raise serializers.ValidationError(f"{seller} is not a seller")
        if attrs["total_quantity"] <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        user = self.context["request"].user
        # from pdb import set_trace; set_trace()
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                {"old_password": ["Wrong password."]}
            )

        # validate_password(new_password)
        return attrs

    def validate_new_password(self, value):
        if self.context["request"].user.check_password(value):
            raise serializers.ValidationError(
                "Password must be different from your old password."
            )
        return value
