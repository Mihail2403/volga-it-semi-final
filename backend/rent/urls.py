from django.urls import path, include
from .views import GetTransportForRentAPIView, GetInfoByIdAPIView, GetMyRentHistory, GetTransportRentHistory, NewRentAPIView, EndRentAPIView

urlpatterns = [
    path('Transport/', GetTransportForRentAPIView.as_view()),
    path('<int:rentid>/', GetInfoByIdAPIView.as_view()),
    path('MyHistory/', GetMyRentHistory.as_view()),
    path('TransportHistory/<int:transportId>/', GetTransportRentHistory.as_view()),
    path('New/<int:transportId>/', NewRentAPIView.as_view()),
    path('End/<int:rentId>/', EndRentAPIView.as_view())
]