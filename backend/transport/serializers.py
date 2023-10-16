from rest_framework import serializers
from accounts.serializers import MyFloatField, AccountSerializer


class TransportTypeSerializer(serializers.Serializer):
    name = serializers.CharField()

class TransportSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    canBeRented = serializers.BooleanField()
    transportType = TransportTypeSerializer()
    model = serializers.CharField(max_length=50)
    color = serializers.CharField(max_length=50)
    identifier = serializers.CharField(max_length=6) # например 'a123bc'
    description = serializers.CharField(max_length=150)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    minutePrice = MyFloatField()
    dayPrice = MyFloatField()
    owner = AccountSerializer()