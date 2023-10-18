from django.db import models

from accounts.models import Account

class TransportType(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name
  


class Transport(models.Model):
    canBeRented = models.BooleanField(default=True)
    transportType = models.ForeignKey(TransportType, on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    identifier = models.CharField(max_length=6, unique=True) # например 'a123bc'
    description = models.CharField(max_length=150, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    minutePrice = models.IntegerField(null=True)
    dayPrice = models.IntegerField(null=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.identifier