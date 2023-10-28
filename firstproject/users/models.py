from django.db import models
from django.contrib.auth import get_user_model
from .validators import phone_number_regex
from common.models import TimeStampedModel

User = get_user_model()

# Create your models here.
class UserAdditional(TimeStampedModel):
    # useradditional
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="additional")
    # a number should have only digits, min length should be 10
    phone_number = models.CharField(max_length=10, validators=[phone_number_regex])