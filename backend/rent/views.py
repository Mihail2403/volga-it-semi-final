import datetime
from math import ceil
from django.db import IntegrityError
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import F, FloatField, functions, Value
from django.utils.datastructures import MultiValueDictKeyError

from backend.errorCheck import rentErrCheck
from accounts.models import Account
from .permissions import IsRenter, IsRenterOrOwner
from transport.permissions import IsAuthAndNotOwner, IsOwnerOrNotAllow
from transport.serializers import TransportSerializer
from transport.models import Transport, TransportType

from .models import Rent, RentType
from .serializers import RentSerializer

def finalPriceCalc(rent, priceOfUnit=None, priceType=None):
    seconds = (rent.date_stop.replace() - rent.date_started.replace()).total_seconds()
    minutes = ceil(seconds / 60)
    days = ceil(seconds / 86400)
    print(minutes)
    print(days)
    finalPrice = None
    if priceOfUnit and priceType:
        print(1)
        if priceType == 'Minutes':
            finalPrice = minutes*priceOfUnit*100
        elif priceType=='Days':
            finalPrice = days*priceOfUnit*100
    elif rent.rentType.name == "Minutes" and rent.transport.minutePrice:
        finalPrice = minutes*rent.transport.minutePrice 
    elif rent.rentType.name == "Days" and rent.transport.dayPrice:
        finalPrice = rent.transport.dayPrice
    return finalPrice

class GetTransportForRentAPIView(APIView):
    """Получение списка транспорта в указаном радиусе"""
    @rentErrCheck
    def get(self, request):
        # получаем данные о круге поиска
        lat = round(float(request.GET['lat']), 5)
        long = round(float(request.GET['long']), 5)
        radius = round(float(request.GET['radius']), 5)
        
        # тип транспорта
        typeStr = request.GET['type']
        
        # а вот тут магия DjangoORM, если коротко, нахожу весь танспорт, подходящий под описанние
        # функции из модуля django.db.models.functions используются тк стандартные функции для тех действий не работают с объектами, оперируемыми в частности в .annotate()
        if typeStr == "All":
            transportList = Transport.objects.all().annotate(
                        distance=
                        # округляю до 5 знаков после запятой
                        functions.Round(
                            # корень
                            functions.Sqrt(
                                # помещаю итог в поле FloatField
                                functions.Cast(
                                        (lat - F('latitude'))**2.0 +
                                        (long - F('longitude'))**2.0,
                                    FloatField()
                                )
                                ), 5
                            )
                    ).filter(
                        canBeRented=True
                    ).filter(
                        distance__lte=radius
                    )
        else:
            transportType = TransportType.objects.get(name=typeStr)
            transportList = Transport.objects.all().annotate(
                        distance=
                        # округляю до 5 знаков после запятой
                        functions.Round(
                            # корень
                            functions.Sqrt(
                                # помещаю итог в поле FloatField
                                functions.Cast(
                                        (lat - F('latitude'))**2.0 +
                                        (long - F('longitude'))**2.0,
                                    FloatField()
                                )
                                ), 5
                            )
                    ).filter(
                        transportType=transportType,
                        canBeRented=True
                    ).filter(
                        distance__lte=radius
                    )
        return response.Response(TransportSerializer(transportList, many=True).data)

class GetInfoByIdAPIView(APIView):
    permission_classes = [IsRenterOrOwner, ]
    @rentErrCheck
    def get(self, request, rentid):
        # получение объекта по id
        rent = Rent.objects.get(id=rentid)
        return response.Response(RentSerializer(rent).data)
        
class GetMyRentHistory(APIView):
    permission_classes = [IsAuthenticated, ]
    @rentErrCheck
    def get(self, request):
        account = Account.objects.get(user=request.user)
        rent = Rent.objects.filter(account=account)
        return response.Response(RentSerializer(rent, many=True).data)
        
class GetTransportRentHistory(APIView):
    permission_classes = [IsOwnerOrNotAllow, ]
    @rentErrCheck
    def get(self, request, transportId):
        transport = Transport.objects.get(id=transportId)
        self.check_object_permissions(
            request=request,
            obj=transport
        )
        rent = Rent.objects.filter(transport=transport)
        return response.Response(RentSerializer(rent, many=True).data)
    
class NewRentAPIView(APIView):
    """Создание новой аренды транспорта"""
    permission_classes = [IsAuthAndNotOwner, ]
    @rentErrCheck
    def post(self, request, transportId):
        transport = Transport.objects.get(id=transportId)
        self.check_object_permissions(
            request=request,
            obj=transport
        )
        rentType = RentType.objects.get(
                name=request.data['rentType']
            )
        account = Account.objects.get(user=request.user)
        if transport.canBeRented:
            if (rentType.name=="Minutes" and transport.minutePrice>0) or (rentType.name == "Days" and transport.dayPrice>0):
                rent = Rent.objects.create(
                    rentType = rentType,
                    account = account,
                    transport = transport,
                    date_started = datetime.datetime.now(),
                    date_stop = None,
                    finalPrice = None
                    )

                # запрет арендовать уже арендованный транспорт 
                transport.canBeRented = False
                transport.save()
                return response.Response(RentSerializer(rent).data)
        return response.Response({
            "err": "this transport can't be rented",
            "err_code":"cant_rented"
        },
        status=400
        )

class EndRentAPIView(APIView):
    """Окончание существующей аренды"""
    permission_classes=[IsRenter, ]
    @rentErrCheck
    def post(self, request, rentId):
        rent = Rent.objects.get(id=rentId)
        self.check_object_permissions(
            request=request,
            obj=rent
        )
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
