from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    amount = models.FloatField()
    currency = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"{self.amount}_{self.currency}"
    
    @property
    def holder_username(self):
        return self.user.username
    
    class Meta:
        permissions = (
            ('can_make_transfers', 'can make transfers'),
            ('can_deposit_funds', 'can deposit funds')
        )
    

# admin => 5 accounts

# sum of amounts present in all the accounts in our system
# select * from account SUM(currency);
# select SUM(Amount) from account where currency="inr";

# sum of amounts in specific currency

# inr => amount = 100
# usd => amount = 200
# group_by clause => values