from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from decimal import Decimal

class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('100000.00'),
        help_text="User's balance in $NUC tokens"
    )
