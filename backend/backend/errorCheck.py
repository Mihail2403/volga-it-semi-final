from transport.models import TransportType
from django.db import DataError, IntegrityError
from rest_framework import response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import F, FloatField, functions, Value
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.exceptions import APIException

from accounts.models import Account
from transport.permissions import IsAuthAndNotOwner, IsOwner
from transport.serializers import TransportSerializer
from transport.models import Transport, TransportType
from rent.models import Rent, RentType
from rent.serializers import RentSerializer


def rentErrCheck(func):
    """Декоратор для проверки на ошибку RentController"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except Account.DoesNotExist:
            return response.Response({
                "err": "Account not exist",
                "err_code":"account_not_exist"
            },
            status=400
            )
        except Transport.DoesNotExist:
            return response.Response({
                "err": "Transport not exist",
                "err_code":"transport_not_exist"
            },
            status=400
            )
        except TransportType.DoesNotExist:
            return response.Response({
                "err": "transportType may be Car\Bike\Scooter",
                "err_code": "transport_type_not_exist"
            },
            status=400
            )
        except Rent.DoesNotExist:
            # если нет объекта по id
            return response.Response({
                "err": "Not found rent on this id",
                "err_code":"rent_doesnt_exist"
            },
            status=400
            )
        except RentType.DoesNotExist:
            return response.Response({
                "err": "rentType may be Minutes\Days",
                "err_code": "transport_type_not_exist"
            },
            status=400
            )
        except APIException:
            return response.Response({
                "err": "You dont have permissions on this action",
                "err_code":"havent_permission"
            },
            status=400
            )
        except TypeError as ex:
            print(ex)
            return response.Response({
                "err": "type error",
                "err_code":"type_err"
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
        except KeyError:
            return response.Response({
                "err": "you don't, give me whats", 
                "err_code":"not_uname_or_pass"
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
    return wrapper

def accErrCheck(func):
    """Декоратор для проверки на ошибку AccountController"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except KeyError:
            return response.Response({
                "err": "you don't, give me whats", 
                "err_code":"not_uname_or_pass"
            },
            status=400
            )

        except IntegrityError:
            return response.Response({
                "err": "field 'username' must be unique", 
                "err_code":"uname_not_unique"
            },
            status=400
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
        except Account.DoesNotExist:
            return response.Response({
                "err": "Account about id does not exist",
                "err_code": "acc_doesnt_exist"
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
    return wrapper

def transportErrCheck(func):
    """Декоратор для проверки на ошибку TransportController"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Transport.DoesNotExist:
            return response.Response({
                    "err": "Transport about id does not exist",
                    "err_code": "transport_doesnt_exist"
                },
                status=400
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
        except APIException:
            return response.Response({
                "err": "You dont have permissions on this action",
                "err_code":"havent_permission"
            },
            status=400
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
    return wrapper

def paymentErrCheck(func):
    """Декоратор для проверки на ошибку TransportController"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Account.DoesNotExist:
            return response.Response({
                "err": "account with this id not exists",
                "err_code": "account_not_exist"
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
    return wrapper
