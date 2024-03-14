from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from sesame.views import LoginView

from .views import (
    CategoryViewSet,
    InventoryViewSet,
    LogoutView,
    OrderViewSet,
    ProductViewSet,
    ProfileViewSet,
    RegisterView,
    ReviewViewSet,
    ShopViewSet,
    UserViewSet,
    index,
)

router = routers.DefaultRouter()
router.register("user", UserViewSet),
router.register("profile", ProfileViewSet)
router.register("shop", ShopViewSet)
router.register("order", OrderViewSet)
router.register("review", ReviewViewSet)
router.register("product", ProductViewSet)
router.register("category", CategoryViewSet)
router.register("inventory", InventoryViewSet)

urlpatterns = router.urls

urlpatterns = [
    path("", index),
    path("api/", include(router.urls)),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/auth/", LoginView.as_view(), name="login"),
    path("api/login/refresh/", TokenRefreshView.as_view()),
    path("api/logout/", LogoutView.as_view(), name="logout"),
]
