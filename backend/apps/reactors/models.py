from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Reactor(models.Model):

    REACTOR_CHOICES = [
        ('nuwave', 'NuWave'),
        ('phoenix_regenx7', 'Phoenix RegenX-7'),
        ('nexus_core', 'Nexus CORE'),
        ('fermi_ii', 'Fermi-II'),
        ('helios_fusiondrive', 'Helios FusionDrive'),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=50, choices=REACTOR_CHOICES, unique=True)
    description = models.TextField()
    location = models.CharField(max_length=100)

    price_per_token = models.DecimalField(
        max_digits=10,
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Price per $NUC token investment"
    )

    annual_roi_rate = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        help_text="Annual ROI as decimal, can be negative (ex: 0.0650 = 6.5%)"
    )

    carbon_offset_per_token_per_year = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0000'))],
        help_text="Tons of CO2 offset per token per year"
    )

    total_token_capacity = models.PositiveIntegerField(
        help_text="Maximum number of tokens that can be invested across all users"
    )

    current_investments = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=Decimal('0.00'),
        help_text="Total tokens currently invested in this reactor"
    )

    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Nuclear Reactor"
        verbose_name_plural = "Nuclear Reactors"

    def __str__(self):
        return f"{self.name} ({self.location})"
    
    