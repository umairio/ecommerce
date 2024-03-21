from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .constants import OrderStatus, ProfileRole
from .models import Inventory, Order, Product, Profile, Review, Shop, User
from .permissions import OwnerPermission, SellerPermission
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
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.object.set_password(serializer.data.get("new_password"))
        self.object.save()
        response = {
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": "Password updated successfully",
            "data": [],
        }
        return Response(response)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            sales_count = instance.order_product.count()
            return Response(
                {"product_id": instance.id, "sales_count": sales_count},
                status=status.HTTP_200_OK,
            )
        except Product.DoesNotExist:
            return Response(
                "Product not found", status=status.HTTP_404_NOT_FOUND
            )

    def list(self, request, *args, **kwargs):
        shop_id = request.query_params.get("shop_id", None)
        if not shop_id:
            return Response(
                {"detail": "shop_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = Product.objects.filter(shop_id=shop_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        buyer_id = request.query_params.get("buyer_id")
        if not buyer_id:
            return Response(
                {"detail": "buyer_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            buyer = Profile.objects.get(id=buyer_id, role=ProfileRole.BUYER)
        except Profile.DoesNotExist:
            return Response(
                {"detail": "Invalid buyer_id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.get_queryset().filter(buyer=buyer)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == OrderStatus.CART:
            self.perform_destroy(instance)
            return Response(
                f"{instance} deleted", status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                {"detail": "Cannot delete confirmed orders."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ShopViewSet(ModelViewSet):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()
    permission_classes = [IsAuthenticated, OwnerPermission]


class InventoryViewSet(ModelViewSet):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()
    permission_classes = [IsAuthenticated, SellerPermission]


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
