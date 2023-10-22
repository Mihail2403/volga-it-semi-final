from typing import Dict, Any

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from accounts.models import Account

# меняю стандартный класс-сериализатор, чтобы получать в ответе только access token (по ТЗ)
class AccessJWTTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        del data['refresh']
        return data

class MyFloatField(serializers.IntegerField):
    def to_representation(self, value):
        return value/100

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    is_staff = serializers.BooleanField()

class AccountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserSerializer()
    balance = MyFloatField()