from rest_framework import serializers
from accounts.serializers import AccountSerializer, MyFloatField
from transport.serializers import TransportSerializer

class RentTypeSerializer(serializers.Serializer):
    name = serializers.CharField()

class RentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    account = AccountSerializer()
    transport = TransportSerializer()
    date_started = serializers.DateTimeField()
    date_stop = serializers.DateTimeField()
    rentType = RentTypeSerializer()
    finalPrice = MyFloatField()