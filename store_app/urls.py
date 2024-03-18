from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from sesame.views import LoginView

from . import views

router = routers.DefaultRouter()
router.register("user", views.UserViewSet),
router.register("profile", views.ProfileViewSet)
router.register("shop", views.ShopViewSet)
router.register("order", views.OrderViewSet)
router.register("review", views.ReviewViewSet)
router.register("product", views.ProductViewSet)
router.register("category", views.CategoryViewSet)
router.register("inventory", views.InventoryViewSet)

urlpatterns = router.urls

urlpatterns = [
    path("", views.index),
    path("api/", include(router.urls)),
    path("api/register/", views.RegisterView.as_view(), name="register"),
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/auth/", LoginView.as_view(), name="login"),
    path("api/login/refresh/", TokenRefreshView.as_view()),
    path("api/logout/", views.LogoutView.as_view(), name="logout"),
    path("api/change-password/", views.ChangePasswordView.as_view()),
]
