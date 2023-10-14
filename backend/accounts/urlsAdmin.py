from django.urls import path

from accounts.viewsAdmin import AccountDetailAPIView, AccountListAPIView


urlpatterns = [
    path('', AccountListAPIView.as_view()),
    path('<int:id>', AccountDetailAPIView.as_view())
]
