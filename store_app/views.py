from django.db.models import F
from django.shortcuts import render
from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import (
    GenericViewSet,
    ModelViewSet,
    ReadOnlyModelViewSet,
)
from rest_framework_simplejwt.tokens import RefreshToken

from .constants import OrderStatus, ProfileRole
from .models import Inventory, Order, Product, Profile, Review, Shop, User
from .permissions import IsBuyer, IsOwner, IsSeller
from .serializers import (
    ChangePasswordSerializer,
    InventorySerializer,
    OrderSerializer,
    ProductSerializer,
    ProfileSerializer,
    RegisterSerializer,
    ReviewSerializer,
    ShopSerializer,
    UserSerializer,
)


def index(request):
    return render(request, "index.html")


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        self.object = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.object.set_password(serializer.validated_data["new_password"])
        self.object.save()
        return Response(
            {"message": "Password updated successfully"},
            status=status.HTTP_200_OK,
        )


class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def create(
        self, request, *args, **kwargs
    ):  # for creating own profile not else
        data = request.data
        user = request.user
        data["user"] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):  # role cannot be changed
        data = request.data
        data.pop("role")

        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {"detail": "This is not your profile."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if instance.user == user or instance.role == ProfileRole.ADMIN:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(
                {"detail": "This is not your profile."},
                status=status.HTTP_403_FORBIDDEN,
            )


class ReviewViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsBuyer]
        self.check_permissions(request)
        order = request.data.get("order")
        user = request.user
        if Order.objects.filter(id=order, buyer__user__email=user).exists():
            request.data["product"] = Order.objects.get(id=order).product.id
            return super().create(request, *args, **kwargs)
        else:
            return Response(
                {"detail": "This order does not belong to you."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsOwner]
        self.check_permissions(request)
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        productId = request.query_params.get("product")
        orderId = request.query_params.get("order")
        if orderId:
            self.queryset = self.queryset.filter(order=orderId)
        if productId:
            self.queryset = self.queryset.filter(product=productId)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsSeller]
        self.check_permissions(request)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsSeller]
        self.check_permissions(request)
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            sales_count = instance.order_product.count()
            return Response(
                {
                    "id": instance.id,
                    "name": instance.name,
                    "description": instance.description,
                    "category": instance.category.name,
                    "sales_count": sales_count,
                    "rating": instance.rating,
                    "shop": instance.shop.name,
                    "seller": instance.seller.user.email,
                    "price": instance.price,
                },
                status=status.HTTP_200_OK,
            )
        except Product.DoesNotExist:
            return Response(
                "Product not found", status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, *args, **kwargs):
        self.permission_classes = [IsSeller]
        self.check_permissions(request)
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.profile.role == ProfileRole.SELLER:
            queryset = Product.objects.filter(seller__user__email=user)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if user.profile.role == ProfileRole.OWNER:
            queryset = Product.objects.filter(shop__owner__user__email=user)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return super().list(request, *args, **kwargs)


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsBuyer]
        self.check_permissions(request)
        product = request.data.get("product")
        quantity = request.data.get("quantity")
        product = Product.objects.get(id=product)
        item_stock = Inventory.objects.get(product=product.id).total_quantity
        if item_stock < int(quantity):
            return Response(
                "Insufficient stock", status=status.HTTP_400_BAD_REQUEST
            )
        Inventory.objects.filter(product=product).update(
            total_quantity=F("total_quantity") - quantity
        )
        request.data["buyer"] = request.user.id
        request.data["seller"] = product.seller.id
        request.data["shop"] = product.shop.id
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.profile.role == ProfileRole.BUYER:
            buyer = user.profile
            queryset = self.get_queryset().filter(buyer=buyer)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if user.profile.role == ProfileRole.SELLER:
            seller = user.profile
            queryset = self.get_queryset().filter(seller=seller)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if user.profile.role == ProfileRole.OWNER:
            owner = user.profile
            queryset = self.get_queryset().filter(shop__owner=owner)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            buyer = user.profile
            queryset = self.get_queryset().filter(buyer=buyer)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user)
        instance = self.get_object()
        if user.profile.role == ProfileRole.BUYER:
            if instance.buyer == user.profile:
                return super().retrieve(request, *args, **kwargs)
        if user.profile.role == ProfileRole.SELLER:
            if instance.seller == user.profile:
                return super().retrieve(request, *args, **kwargs)
        if user.profile.role == ProfileRole.OWNER:
            if instance.shop.owner == user.profile:
                return super().retrieve(request, *args, **kwargs)
        if user.profile.role == ProfileRole.ADMIN:
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response(
                {"detail": "Cannot view orders not belonging to you."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != OrderStatus.CART:
            return Response(
                {"detail": "Cannot delete confirmed orders."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (
            self.request.user.profile.role == ProfileRole.BUYER
            and instance.buyer != self.request.user.profile
        ):
            return Response(
                {"detail": "Cannot delete orders not belonging to you."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_destroy(instance)
        return Response(
            f"{instance} deleted", status=status.HTTP_204_NO_CONTENT
        )

    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if user.profile.role == ProfileRole.BUYER:
            if (
                instance.status == OrderStatus.CART
                and instance.buyer == user.profile
            ):
                return super().update(request, *args, **kwargs)
            else:
                return Response(
                    {"detail": "Cannot update confirmed orders."},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class ShopViewSet(ModelViewSet):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()
    permission_classes = [IsOwner]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if (
            instance.owner.user != request.user
            or request.user.profile.role != ProfileRole.ADMIN
        ):
            return Response(
                {"detail": "You are not authorized to update this shop."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if (
            instance.owner.user != request.user
            or request.user.profile.role != ProfileRole.ADMIN
        ):
            return Response(
                {"detail": "You are not authorized to delete this shop."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):

        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return super().retrieve(request, *args, **kwargs)


class InventoryViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()
    permission_classes = [IsOwner]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if (
            instance.shop.owner.user != request.user
            or request.user.profile.role != ProfileRole.ADMIN
        ):
            return Response(
                {"detail": "This is not your inventory."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if (
            instance.shop.owner.user != request.user
            or request.user.profile.role != ProfileRole.ADMIN
        ):
            return Response(
                {"detail": "This is not your inventory."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if request.user.profile.role == ProfileRole.ADMIN:
            return super().list(request, *args, **kwargs)
        serializer = self.get_serializer(
            self.get_queryset().filter(shop__owner__user__email=request.user),
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if (
            instance.shop.owner.user != request.user
            or request.user.profile.role != ProfileRole.ADMIN
        ):
            return Response(
                {"detail": "This is not your inventory."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().retrieve(request, *args, **kwargs)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")

        if not refresh:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh)
            token.blacklist()
            return Response(
                {"message": "Logout successful."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
