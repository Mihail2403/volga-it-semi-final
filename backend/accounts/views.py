from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from accounts.models import Account

class MeAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        try:
            user = request.user
            account = Account(user=user)
            return response.Response({
                "person": {
                    "id":account.id,
                    "username": user.username,
                    "balance":account.balance,
                }
            })
        except Exception as ex:
            print(ex)
            return response.Response({
                "err": "unknown error on server", 
                "err_code":"unknown_serv_err"
            })


class SignUpAPIView(APIView):
    def post(self, request):
        try:
            uname = request.data['username']
            password = request.data['password']
            account = Account.objects.create(
                user=User.objects.create_user(username=uname, password=password)
                )
            return response.Response({
                "person": {
                    "id": account.id,
                    "name": account.user.username,
                    "balance": account.balance
                }
            })
        
        except KeyError:
            return response.Response({
                "err": "you don't, give me 'username' or 'password'", 
                "err_code":"not_uname_or_pass"
            })

        except IntegrityError:
            return response.Response({
                "err": "field 'username' must be unique", 
                "err_code":"uname_not_unique"
            })
        
        except Exception as ex:
            print(ex)
            return response.Response({
                "err": "unknown error on server", 
                "err_code":"unknown_serv_err"
            })

class UpdateAccAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def put(self, request):
        try:
            user = request.user
            user.username = request.data['username']
            user.set_password(request.data['password'])
            user.save()
            return response.Response({
                "person": {
                    "id": Account.objects.get(user=user).id,
                    "name": user.username,
                    "balance": Account.objects.get(user=user).balance
                }
            })
        
        except KeyError:
            return response.Response({
                "err": "you don't, give me 'username' or 'password'", 
                "err_code":"not_uname_or_pass"
            })

        except IntegrityError:
            return response.Response({
                "err": "field 'username' must be unique", 
                "err_code":"uname_not_unique"
            })
        
        except Exception as ex:
            print(ex)
            return response.Response({
                "err": "unknown error on server", 
                "err_code":"unknown_serv_err"
            })
