from django.urls import include, path
from .viewsAdmin import RentDetailView, UserHistoryAPIView, TransportRentHistory, NewRentAPIView, EndRentAPIView


urlpatterns = [
    path('<int:rentId>/', RentDetailView.as_view()),
    path('', NewRentAPIView.as_view()),
    path('End/<int:rentId>/', EndRentAPIView.as_view())
]
