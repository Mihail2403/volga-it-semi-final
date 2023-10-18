from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError

from accounts.models import Account
from accounts.serializers import AccountSerializer


class AccountListAPIView(APIView):
    permission_classes = [IsAdminUser, ]
    def get(self, request):
        try:
            start = int(request.GET['start'])
            count = int(request.GET['count'])
            queryset = Account.objects.filter(id__gt=start)[:count]
            return response.Response(
                AccountSerializer(queryset, many=True).data
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
            user = User.objects.create_user(
                username=request.data['username'],
                password=request.data['password'],
                is_staff = request.data['isAdmin'],
            )
            account = Account.objects.create(
                user=user,
                balance=int(request.data['balance']*100)
            )
            return response.Response(
                AccountSerializer(account).data
            )
        
        except KeyError:
            return response.Response({
                "err": "you don't, give me 'username' or 'password' or 'isAdmin' or 'balance'", 
                "err_code":"not_uname_or_pass"
            },
            status=400
            )

        except ValueError:
            return response.Response({
                "err": "'balance' must be double type",
                "err_code": "incorrect_type_of_balance"
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
        
        except Exception as ex:
            print(ex)
            return response.Response({
                "err": "unknown error on server", 
                "err_code":"unknown_serv_err"
            },
            status=400
            )
    
class AccountDetailAPIView(APIView):
    permission_classes = [IsAdminUser, ]
    def get(self, request, id):
        try:
            account = Account.objects.get(id=id)
            return response.Response(AccountSerializer(account).data)
        
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
        
    def put(self, request, id):
        
        try:
            account = Account.objects.get(id=id)
            user = account.user
            
            user.username = request.data['username']
            user.set_password(request.data['password'])
            user.is_staff = request.data['isAdmin']
            user.save()

            account.balance = request.data['balance']
            account.save()
            
            return response.Response({
                "person": {
                    "id": Account.objects.get(user=user).id,
                    "name": user.username,
                    "balance": Account.objects.get(user=user).balance
                }
            })
        
        except KeyError:
            return response.Response({
                "err": "you don't, give me 'username' or 'password' or 'isAdmin' or 'balance'", 
                "err_code":"not_uname_or_pass"
            },
            status=400
            )

        except IntegrityError:
            return response.Response({
                "err": "field 'username' must be unique", 
                "err_code":"uname_not_unique"
            })

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


    def delete(self, request, id):
        try:

            account = Account.objects.get(id=id)
            account.user.delete()
            account.delete()
            return response.Response({})

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
        