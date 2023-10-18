import math
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import F, FloatField, functions, Value
from transport.serializers import TransportSerializer
from transport.models import Transport, TransportType
from django.utils.datastructures import MultiValueDictKeyError

from .models import Rent
from .serializers import RentSerializer

class GetTransportForRentAPIView(APIView):
    def get(self, request):
        try:
            # получаем данные о круге поиска
            lat = round(float(request.GET['lat']), 5)
            long = round(float(request.GET['long']), 5)
            radius = round(float(request.GET['radius']), 5)
            # тип транспорта
            typeStr = request.GET['type']
            transportType = TransportType.objects.get(name=typeStr)
            # а вот тут магия DjangoORM, если коротко, нахожу весь танспорт, подходящий под описанние
            transportList = Transport.objects.all().annotate(
                        distance=
                        functions.Round(
                            functions.Sqrt(
                              functions.Cast(
                                        (lat - F('latitude'))**2.0 +
                                        (long - F('longitude'))**2.0,
                                    FloatField()
                                )
                              ), 5
                            )
                    ).filter(
                        distance__lte=radius
                    ).filter(
                        transportType=transportType
                    )
            print(transportList[0].distance)
            return response.Response(TransportSerializer(transportList, many=True).data)
        
        # если тип транспорта не ожидаемый
        except TransportType.DoesNotExist:
            return response.Response({
                "err": "transportType may be Car\Bike\Scooter",
                "err_code": "transport_type_not_exist"
            },
            status=400
            )
        # если не передан один из параметров
        except MultiValueDictKeyError:
            return response.Response({
                "err": "Give me 'lat', 'long' and 'type' named params",
                "err_code": "didnt_given_param"
            },
            status=400
            )
        # если в параметрах не числа
        except ValueError:
            return response.Response({
                "err": "You make mistake on types values? which you give me",
                "err_code": "type err"
            },
            status=400
            )
        except Exception as ex:
            print(ex)
            return response.Response({
                "err": "unknown error on server", 
                "err_code":"unknown_serv_err"
            },
            status=400
            )

class GetInfoByIdAPIView(APIView):
    def get(self, request, rentid):
        try:
            # получение объекта по id
            rent = Rent.objects.get(id=rentid)
            return response.Response(RentSerializer(rent).data)
        except Rent.DoesNotExist:
            # если нет объекта по id
            return response.Response({
                "err": "Not found rent on this id", 
                "err_code":"rent_doesnt_exist"
            },
            status=400
            )
        except Exception as ex:
            print(ex)
            return response.Response({
                "err": "unknown error on server", 
                "err_code":"unknown_serv_err"
            },
            status=400
            )
