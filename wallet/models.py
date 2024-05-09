from django.db import models

class Wallet(models.Model):
    user = models.CharField(max_length=200, default="")
    quantity = models.FloatField()
    quantityBetLocked = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user} {self.quantity}"
    
class WalletHistory(models.Model):
    user = models.CharField(max_length=200, default="")
    quantity = models.FloatField()
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.quantity} {self.description}"