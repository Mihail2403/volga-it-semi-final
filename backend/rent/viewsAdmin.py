import datetime
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from accounts.models import Account

from backend.errorCheck import rentErrCheck
from rent.views import finalPriceCalc
from transport.models import Transport, TransportType

from .models import Rent, RentType
from .serializers import RentSerializer

class RentDetailView(APIView):
    permission_classes = [IsAdminUser, ]
    @rentErrCheck
    def get(self, request, rentId):
        """Получение инфо о аренде по id"""
        rent = Rent.objects.get(id=rentId)
        return response.Response(RentSerializer(rent).data)

    @rentErrCheck
    def put(self, request, rentId):
        """Изменение аренды по id"""
        rent = Rent.objects.get(id=rentId)
        transportId = request.data['transportId']
        userId = request.data['userId']
        timeStart = datetime.datetime.fromisoformat(request.data['timeStart'])
        timeEnd = datetime.datetime.fromisoformat(request.data['timeEnd']) if request.data.get('timeEnd') else None
        priceOfUnit = request.data['priceOfUnit']
        priceType = request.data['priceType']
        finalPrice = request.data.get('finalPrice')
        
        rent.transport = Transport.objects.get(id=transportId)
        rent.account = Account.objects.get(id=userId)
        rent.date_started = timeStart
        rent.date_stop = timeEnd
        rent.rentType = RentType.objects.get(name=priceType)
        rent.finalPrice = finalPriceCalc(rent, priceOfUnit, priceType) if timeEnd else None
        rent.save()
        print(finalPrice)

        return response.Response(RentSerializer(rent).data)
    
    @rentErrCheck
    def delete(self, request, rentId):
        """Удаление аренды по id"""
        rent = Rent.objects.get(id=rentId)
        rent.delete()
        return response.Response({})
    
class UserHistoryAPIView(APIView):
    permission_classes = [IsAdminUser, ]
    @rentErrCheck
    def get(self, request, userId):
        """Получение истории аренд пользователя"""
        account = Account.objects.get(user=userId)
        rent = Rent.objects.filter(account=account)
        return response.Response(RentSerializer(rent, many=True).data)

class TransportRentHistory(APIView):
    permission_classes = [IsAdminUser, ]
    @rentErrCheck
    def get(self, request, transportId):
        """Получение истории аренд транспортного средства"""
        transport = Transport.objects.get(id=transportId)
        rent = Rent.objects.filter(transport=transport)
        return response.Response(RentSerializer(rent, many=True).data)

class NewRentAPIView(APIView):
    permission_classes = [IsAdminUser, ]
    @rentErrCheck
    def post(self, request):
        """Создание аренды"""
        transportId = request.data['transportId']
        userId = request.data['userId']
        timeStart = datetime.datetime.fromisoformat(request.data['timeStart'])
        timeEnd = datetime.datetime.fromisoformat(request.data['timeEnd']) if request.data.get('timeEnd') else None
        priceOfUnit = request.data['priceOfUnit']
        priceType = request.data['priceType']
        finalPrice = request.data.get('finalPrice')
        rent = Rent.objects.create(
            account=Account.objects.get(id=userId),
            rentType = RentType.objects.get(name=priceType),
            transport = Transport.objects.get(id=transportId),
            date_started = timeStart, 
            date_stop = timeEnd
        )
        rent.finalPrice = finalPriceCalc(rent, priceOfUnit, priceType) if timeEnd else None
        rent.save()
        return response.Response(RentSerializer(rent).data)

class EndRentAPIView(APIView):
    permission_classes=[IsAdminUser, ]
    @rentErrCheck
    def post(self, request, rentId):
        """Завершение аренды по id"""
        rent = Rent.objects.get(id=rentId)
        if not rent.date_stop:
            rent.transport.canBeRented = True
            rent.transport.latitude = request.data['lat']
            rent.transport.longitude = request.data['long']
            rent.transport.save()
            rent.date_stop = datetime.datetime.now()
            rent.save()
            if finalPriceCalc(rent=rent):
                rent.finalPrice = finalPriceCalc(rent)
                rent.save()
            else:
                return response.Response({
                    "err": "Err of calc finalPrice",
                    "err_code":"calc_finalprice_err"
                },
                status=400
                )
        return response.Response(RentSerializer(rent).data)
