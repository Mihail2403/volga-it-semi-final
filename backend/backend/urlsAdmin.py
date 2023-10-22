from django.urls import include, path

from accounts import urlsAdmin as accountUrls
from rent.viewsAdmin import TransportRentHistory, UserHistoryAPIView
from transport import urlsAdmin as transportUrls
from rent import urlsAdmin as rentUrls
urlpatterns = [
    path('Account/', include(accountUrls.urlpatterns)),
    path('Transport/', include(transportUrls.urlpatterns)),
    path('Rent/', include(rentUrls.urlpatterns)),
    path('UserHistory/<int:userId>/', UserHistoryAPIView.as_view()),
    path('TransportHistory/<int:transportId>/', TransportRentHistory.as_view()),
]