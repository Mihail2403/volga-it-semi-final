from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import response
from accounts.models import Account
from backend.errorCheck import paymentErrCheck
# Create your views here.
class PaymentHesoyamAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    @paymentErrCheck
    def post(self, request, accountId):
        """Добавление к балансу пользователя 250'000 денежных единиц"""
        if request.user.is_staff:
            acc = Account.objects.get(id=accountId)
            acc.balance+=(250000*100)
            acc.save()
        else:
            acc = Account.objects.get(user=request.user)
            acc.balance+=(250000*100)
            acc.save()
        return response.Response({})
