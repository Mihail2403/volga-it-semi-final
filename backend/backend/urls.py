# from django.contrib import admin
from django.urls import path, include
from accounts import urls as accUrls
from . import urlsAdmin 
from transport import urls as transportUrls
from rent import urls as rentUrls
from payment import urls as payUrls
from docs import urls as docsUrls
urlpatterns = [
    # path('admin/', admin.site.urls),
    
    path('api/Admin/', include(urlsAdmin.urlpatterns)),
    
    path('api/Accounts/', include(accUrls.urlpatterns)),
    path('api/Transport/', include(transportUrls.urlpatterns)),
    path('api/Rent/', include(rentUrls.urlpatterns)),
    path('api/Payment/', include(payUrls.urlpatterns)),

    path("", include(docsUrls.urlpatterns)),
]
