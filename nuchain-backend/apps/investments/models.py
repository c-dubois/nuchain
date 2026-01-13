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
        help_text="Amount of $NUC invested in this reactor"
    ) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Investment"
        verbose_name_plural = "Investments"
    
    def __str__(self):
        return f"{self.user.username} → {self.reactor.name}: {self.amount_invested:,.2f} $NUC invested"