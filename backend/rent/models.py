from django.db import models
from accounts.models import Account
from transport.models import Transport

class RentType(models.Model):
    name = models.CharField(max_length=10)
    def __str__(self) -> str:
        return self.name

class Rent(models.Model):
    rentType = models.ForeignKey(RentType, on_delete=models.CASCADE, null=True, default=None)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    date_started = models.DateTimeField()
    date_stop = models.DateTimeField(null=True)
    finalPrice = models.IntegerField(null=True, default=None)

    def __str__(self):
        return f"{self.account.user.username} - {self.transport.model}" 
