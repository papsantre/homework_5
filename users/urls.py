from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import (
    UserViewSet,
    PaymentCreateAPIView,
    PaymentListAPIView,
    UserCreateAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

router = DefaultRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("list/", UserListAPIView.as_view(), name="users_list"),
    path("retrieve/<int:pk>/", UserRetrieveAPIView.as_view(), name="users_retrieve"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="users_update"),
    path("destroy/<int:pk>/", UserDestroyAPIView.as_view(), name="users_destroy"),
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path("payment/list/", PaymentListAPIView.as_view(), name="payment_list"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
] + router.urls
