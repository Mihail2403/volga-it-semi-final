from django.db import models
from accounts.models import Account
from transport.models import Transport


class Rent(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)
    date_started = models.DateTimeField()
    date_stop = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.account.user.username} - {self.transport.model}" 
