from django.db import DataError, IntegrityError
from rest_framework.views import APIView
from rest_framework import response
from rest_framework.permissions import IsAdminUser
from django.utils.datastructures import MultiValueDictKeyError

from accounts.models import Account
from .serializers import TransportSerializer
from .models import Transport, TransportType


class TransportListAndAddAPIView(APIView):
    permission_classes = [IsAdminUser, ]
    def get(self, request):
        try:
            start = int(request.GET['start'])
            count = int(request.GET['count'])
            queryset = Transport.objects.filter(id__gt=start)[:count]
            return response.Response(
                TransportSerializer(queryset, many=True).data
            )
        except MultiValueDictKeyError:
            return response.Response({
                "err": "you dont give 'start' or 'count'",
                "err_code": "not_start_or_count"
            },
            status=400
            )
        
        except ValueError:
            return response.Response({
                "err": "'start' and 'count' must be integer type",
                "err_code": "incorrect_start_or_count"
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
        
    def post(self, request):
        try:
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
                    minutePrice=minutePrice if minutePrice else 0,
                    dayPrice=dayPrice if dayPrice else 0,
                    owner=owner
                )
                return response.Response(TransportSerializer(transportNew).data)
        
        except IntegrityError:
            # identifier не уникален
            if Transport.objects.filter(identifier=request.data.get('identifier')).exists():  
                return response.Response({
                    "err": "field 'identifier' must be unique",
                    "err_code":"identifier_not_unique"
                },
            status=400
            )
            
            # если IntegrityError, но identifier уникален
            return response.Response({
                "err": "You give me unexpected value",
                "err_code":"unexpected_value"
            },
            status=400
            )
        # если тип транспорта не ожидаемый
        except TransportType.DoesNotExist:
            return response.Response({
                "err": "transportType may be Car\Bike\Scooter",
                "err_code": "transport_type_not_exist"
            },
            status=400
            )
        except Account.DoesNotExist:
            return response.Response({
                "err": "account with this id not exists",
                "err_code": "account_not_exist"
            },
            status=400
            )
        except TypeError:
            return response.Response({
                "err": "type error",
                "err_code":"type_err"
            },
            status=400
            )
        
        except DataError:
            return response.Response({
                "err": "type error, may be you give the number is too large",
                "err_code":"num_is_too_large"
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

class TransportDetailView(APIView):
    permission_classes = [IsAdminUser, ]
    def get(self, request, id):
        try:
            transport = Transport.objects.get(id=id)
            return response.Response(
                    TransportSerializer(transport).data,
                    status=200
                )
        
        except Transport.DoesNotExist:
            return response.Response({
                    "err": "Transport about id does not exist",
                    "err_code": "transport_doesnt_exist"
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
        
    def put(self, request, id):
        try:
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
                transportNew.minutePrice = minutePrice if minutePrice else 0
                transportNew.dayPrice = dayPrice if dayPrice else 0

                transportNew.save()

                return response.Response(
                    TransportSerializer(transportNew).data,
                    status=200
                    )
        
        except IntegrityError:
            return response.Response({
                "err": "You give me unexpected value",
                "err_code":"unexpected_value"
            },
            status=400
            )
        
        # если тип транспорта не ожидаемый
        except TransportType.DoesNotExist:
            return response.Response({
                "err": "transportType may be Car\Bike\Scooter",
                "err_code": "transport_type_not_exist"
            },
            status=400
            )
        
        except TypeError:
            return response.Response({
                "err": "type error",
                "err_code":"type_err"
            },
            status=400
            )
        except Account.DoesNotExist:
            return response.Response({
                "err": "account with this id not exists",
                "err_code": "account_not_exist"
            },
            status=400
            )
        except DataError:
            return response.Response({
                "err": "type error, may be you give the number is too large",
                "err_code":"num_is_too_large"
            },
            status=400
            )
        except Transport.DoesNotExist:
            return response.Response({
                "err": "Transport with this id not exists",
                "err_code":"transport_not_exists"
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
        
    def delete(self, request, id):
        try:
            transport = Transport.objects.get(id=id)
            transport.delete()
            return response.Response({})

        except Transport.DoesNotExist:
            return response.Response({
                "err": "Transport with this id not exists",
                "err_code":"transport_not_exists"
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