from django.urls import path
from .views import PaymentHesoyamAPIView
urlpatterns = [
    path('Hesoyam/<int:accountId>/', PaymentHesoyamAPIView.as_view())
]