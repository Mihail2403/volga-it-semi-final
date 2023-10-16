from django.urls import include, path

from accounts import urlsAdmin as accountUrls
from transport import urlsAdmin as transportUrls

urlpatterns = [
    path('Account/', include(accountUrls.urlpatterns)),
    path('Transport/', include(transportUrls.urlpatterns))
]