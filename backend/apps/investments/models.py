from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Investment(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='investments'
    )
    reactor = models.ForeignKey(
        'reactors.Reactor',
        on_delete=models.CASCADE,
        related_name='investments'
    )

    amount_invested = models.DecimalField(
        max_digits=10,
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Number of $NUC tokens invested"
    ) 

    time_period_years = models.PositiveIntegerField(
        help_text="Investment time period in years (1, 2, 5, or 10)"
    )