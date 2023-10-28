from django.db import models
from django.contrib.auth import get_user_model
from common.models import SoftDeleteModel, TimeStampedModel

User = get_user_model()


# Create your models here.
class Account(SoftDeleteModel, TimeStampedModel):
    # default reverse lookup => u.account_set.all()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="accounts")
    amount = models.FloatField()
    currency = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"{self.amount}_{self.currency}"

    class Meta:
        permissions = (
            ('can_make_transfers', 'can make transfers'),
            ('can_deposit_funds', 'can deposit funds')
        )

    @property
    def holder_username(self):
        return self.user.username


# admin => 5 accounts