from django.urls import include, path

from accounts import urlsAdmin


urlpatterns = [
    path('Account/', include(urlsAdmin.urlpatterns))
]