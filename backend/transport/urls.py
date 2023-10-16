from django.urls import path

from transport.views import TransportDetailAPIView, TransportAddAPIView


urlpatterns = [
    path('<int:id>/', TransportDetailAPIView.as_view()),
    path('', TransportAddAPIView.as_view())
]
