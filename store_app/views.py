from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

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
from .permissions import ShopPermission
from .serializers import (
    CategorySerializer,
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

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(
                serializer.data.get("old_password")
            ):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]


class ShopViewSet(ModelViewSet):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()
    permission_classes = [IsAuthenticated, ShopPermission]



class InventoryViewSet(ModelViewSet):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()
    permission_classes = [IsAuthenticated]


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


class ShopProductView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):

        pk = bool(self.kwargs)

        if pk is True:
            pk = self.kwargs["pk"]
            return Product.objects.filter(shop=pk)
        
        else:
            owner = self.request.user.profile.id
            shop = Shop.objects.get(owner=owner)
            return Product.objects.filter(shop=shop)