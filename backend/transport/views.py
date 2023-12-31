from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import response
from rest_framework.permissions import IsAuthenticated
from accounts.models import Account
from backend.errorCheck import transportErrCheck
from transport.models import Transport, TransportType
from django.db.utils import DataError
from rest_framework.exceptions import APIException

from .serializers import TransportSerializer
from .permissions import IsOwner


class TransportDetailAPIView(APIView):
    permission_classes = [IsOwner, ]
    @transportErrCheck
    def get(self, request, id):
        """получение информации о транспорте по id"""
        transport = Transport.objects.get(id=id)
        self.check_object_permissions(
            request=request,
            obj=transport
        )
        return response.Response(
                TransportSerializer(transport).data,
                status=200
            )
    
    @transportErrCheck
    def put(self, request, id):
        """Изменение транспорта по id"""
        minutePrice = request.data.get('minutePrice')
        dayPrice = request.data.get('dayPrice')
        if not (minutePrice or dayPrice):
            return response.Response({
                "err": "Set dayPrice or dayPrice please",
                "err_code": "minute_and_day_price_cant_be_null_simultaneous"
            },
            status=400
            )
        else:
            transportNew = Transport.objects.get(id=id)
            
            self.check_object_permissions(
                request=request,
                obj=transportNew
            )

            transportNew.canBeRented = request.data.get('canBeRented', True)
            transportNew.model = request.data.get('model')
            transportNew.color = request.data.get('color')
            transportNew.identifier = request.data.get('identifier')
            transportNew.description = request.data.get('description', "")
            transportNew.latitude = round(request.data.get('latitude'), 5)
            transportNew.longitude = round(request.data.get('longitude'), 5)
            transportNew.minutePrice = int(minutePrice*100) if minutePrice else 0
            transportNew.dayPrice = int(dayPrice*100) if dayPrice else 0

            transportNew.save()

            return response.Response(
                TransportSerializer(transportNew).data,
                status=200
                )
    # удаление
    @transportErrCheck
    def delete(self, request, id):
        """удаление транспорта по id"""
        transport = Transport.objects.get(id=id)
        self.check_object_permissions(request=request, obj=transport)
        transport.delete()
        return response.Response({})

class TransportAddAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    @transportErrCheck
    def post(self, request):
        """добавление нового транспорта"""
        minutePrice = request.data.get('minutePrice')
        dayPrice = request.data.get('dayPrice')
        if not (minutePrice or dayPrice):
            return response.Response({
                "err": "Set dayPrice or dayPrice please",
                "err_code": "minute_and_day_price_cant_be_null_simultaneous"
            },
        status=400
        )
        else:
            owner = Account.objects.get(user=request.user)
            transportType = TransportType.objects.get(
                name=request.data.get('transportType')
            )
            transportNew = Transport.objects.create(
                canBeRented=request.data.get('canBeRented', True),
                transportType=transportType,
                model=request.data.get('model'),
                color=request.data.get('color'),
                identifier=request.data.get('identifier'),
                description=request.data.get('description', ""),
                latitude=round(request.data.get('latitude'), 5),
                longitude=round(request.data.get('longitude'), 5),
                minutePrice=int(minutePrice*100) if minutePrice else 0,
                dayPrice=int(dayPrice*100) if dayPrice else 0,
                owner=owner
            )
            return response.Response(TransportSerializer(transportNew).data)
