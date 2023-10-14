from django.urls import path

from .views import MeAPIView

urlpatterns = [
    path('Me/', MeAPIView.as_view())
]