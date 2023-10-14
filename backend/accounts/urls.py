from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import MeAPIView, SignUpAPIView, UpdateAccAPIView

urlpatterns = [
    # Информация о аккаунте
    path('Me/', MeAPIView.as_view(), name='me'),

    # Вход
    path('SignIn/', TokenObtainPairView.as_view(), name='login'),

    # Регистрация
    path('SignUp/', SignUpAPIView.as_view(), name='signup'),

    # Изменение профиля
    path('Update/', UpdateAccAPIView.as_view())
]