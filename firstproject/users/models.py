from django.db import models
from django.contrib.auth import get_user_model
from .validators import phone_number_regex
User = get_user_model()

# Create your models here.

# Profile / UserAdditional / UserDetail
class UserDetail(models.Model):
    # default reverse => .userdetail
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="detail")
    phone_number = models.CharField(max_length=10, validators=[phone_number_regex])



class CustomPermissions(models.Model):

    class Meta:

        managed = False  # No database table creation or deletion operations will be performed for this model.

        default_permissions = () # disable "add", "change", "delete" and "view" default permissions

        # All the custom permissions not related to models on Manufacturer
        permissions = (
            ('view_operations_dashboard', 'can view operations dashboard'),
            ('perform_transfers', 'can perform transfers')
        )