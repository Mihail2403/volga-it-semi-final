from django.shortcuts import render
from rest_framework import response
from rest_framework.views import APIView


# Create your views here.

class MeAPIView(APIView):
    def get(self, request):
        return response.Response({"Hello":"World"})