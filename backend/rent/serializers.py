from rest_framework import serializers
from accounts.serializers import AccountSerializer
from transport.serializers import TransportSerializer


class RentSerializer(serializers.Serializer):
    account = AccountSerializer()
    transport = TransportSerializer()
    date_started = serializers.DateTimeField()
    date_stop = serializers.DateTimeField()