from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import register_user, user_profile

urlpatterns = [
    # API для регистрации
    path("register/", register_user, name="api_register"),
    # API для JWT токенов
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # API для работы с профилем
    path("profile/", user_profile, name="api_profile"),
]
