from django.urls import path, include
from .views import GetTransportForRentAPIView, GetInfoByIdAPIView

urlpatterns = [
    path('Transport/', GetTransportForRentAPIView.as_view()),
    path('<int:rentid>/', GetInfoByIdAPIView.as_view())
]

