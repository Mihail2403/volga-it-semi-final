"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from accounts import urls as accUrls
from . import urlsAdmin 
from transport import urls as transportUrls
from rent import urls as rentUrls
from payment import urls as payUrls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/Admin/', include(urlsAdmin.urlpatterns)),
    path('api/Accounts/', include(accUrls.urlpatterns)),
    path('api/Transport/', include(transportUrls.urlpatterns)),
    path('api/Rent/', include(rentUrls.urlpatterns)),
    path('api/Payment/', include(payUrls.urlpatterns)),
]

