from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from accounts.models import Account
from .serializers import AccountSerializer
from backend.errorCheck import accErrCheck

class MeAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    @accErrCheck
    def get(self, request):
        user = request.user
        account = Account.objects.get(user=user)
        return response.Response(AccountSerializer(account).data)
        
class SignUpAPIView(APIView):
    @accErrCheck
    def post(self, request):
        uname = request.data['username']
        password = request.data['password']
        account = Account.objects.create(
            user=User.objects.create_user(username=uname, password=password)
            )
        return response.Response(AccountSerializer(account).data)
        
class UpdateAccAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    @accErrCheck
    def put(self, request):
        user = request.user
        user.username = request.data['username']
        user.set_password(request.data['password'])
        user.save()
        account = Account.objects.get(user=user)
        return response.Response(AccountSerializer(account).data)
