from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"uname: {self.user.username}, balance: {self.balance}"
