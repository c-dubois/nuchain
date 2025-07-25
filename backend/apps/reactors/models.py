from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Reactor(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    location = models.CharField(max_length=100)

    cost_per_token = models.DecimalField(
        max_digits=10,
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Cost per $NUC token investment"
    )