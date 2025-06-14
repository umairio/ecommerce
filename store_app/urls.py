from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

router = routers.DefaultRouter()
router.register("profile", views.ProfileViewSet)
router.register("shop", views.ShopViewSet)
router.register("order", views.OrderViewSet)
router.register("review", views.ReviewViewSet)
router.register("product", views.ProductViewSet)
router.register("inventory", views.InventoryViewSet)
router.register("user", views.UserViewSet)

urlpatterns = router.urls

urlpatterns = [
    path("", views.index),
    path("api/", include(router.urls)),
    path("api/authuser/", views.AuthUserView.as_view(), name="authuser"),
    path("api/register/", views.RegisterView.as_view(), name="register"),
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/login/refresh/", TokenRefreshView.as_view()),
    path("api/logout/", views.LogoutView.as_view(), name="logout"),
    path("api/change-password/", views.ChangePasswordView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
