from django.db import DataError, IntegrityError
from rest_framework.views import APIView
from rest_framework import response
from rest_framework.permissions import IsAdminUser
from django.utils.datastructures import MultiValueDictKeyError

from accounts.models import Account
from backend.errorCheck import transportErrCheck
from .serializers import TransportSerializer
from .models import Transport, TransportType


class TransportListAndAddAPIView(APIView):
    permission_classes = [IsAdminUser, ]
    @transportErrCheck
    def get(self, request):
        start = int(request.GET['start'])
        count = int(request.GET['count'])
        transportType = request.GET['transportType']
        if transportType == 'All':
            queryset = Transport.objects.filter(id__gte=start)[:count]
        else: 
            queryset = Transport.objects.filter(
                transportType=TransportType.objects.get(name=transportType)
            ).filter(id__gte=start)[:count]
        return response.Response(
            TransportSerializer(queryset, many=True).data
        )
    @transportErrCheck
    def post(self, request):
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
            owner = Account.objects.get(id=request.data.get('ownerId'))
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

class TransportDetailView(APIView):
    permission_classes = [IsAdminUser, ]
    @transportErrCheck
    def get(self, request, id):
        transport = Transport.objects.get(id=id)
        return response.Response(
                TransportSerializer(transport).data,
                status=200
        )
    @transportErrCheck
    def put(self, request, id):
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
            owner = Account.objects.get(id=request.data.get('ownerId'))
            transportType = TransportType.objects.get(
                name=request.data.get('transportType')
            )

            transportNew.owner = owner
            transportNew.canBeRented = request.data.get('canBeRented', True)
            transportNew.transportType = transportType
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
    @transportErrCheck
    def delete(self, request, id):
        transport = Transport.objects.get(id=id)
        transport.delete()
        return response.Response({})