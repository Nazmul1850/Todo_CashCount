from django.db import models

from django.contrib.auth.models import User

class CashMemo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=20, decimal_places=2,default=0)
    created = models.DateTimeField(auto_now_add=True)
    taken = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class FixBudetModel(models.Model):
    budget = models.DecimalField(max_digits=20, decimal_places=2,default=0)
    userb = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.userb.username
