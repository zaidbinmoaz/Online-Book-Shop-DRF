from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import BookViewSet, Login, RegisterUser, UserDetail

app_name = "api"

router = DefaultRouter()

router.register(r"epicbooks", BookViewSet, basename="books")

urlpatterns = [
    path("", include(router.urls), name="epicbooks"),
    path("register/", RegisterUser.as_view(), name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("profile/", UserDetail.as_view(), name="detail"),
    path("gettoken/", TokenObtainPairView.as_view(), name="token_obtain_view"),
    path("refreshtoken/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verifytoken/", TokenVerifyView.as_view(), name="token_verify"),
]
