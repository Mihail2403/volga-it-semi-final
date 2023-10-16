from django.urls import path
from .viewsAdmin import TransportDetailView, TransportListAndAddAPIView


urlpatterns = [
    path('<int:id>/', TransportDetailView.as_view()),
    path('', TransportListAndAddAPIView.as_view())
]
