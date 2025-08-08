from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Reactor(models.Model):

    REACTOR_CHOICES = [
        ('nuwave', 'NuWave'),
        ('phoenix_regenx7', 'Phoenix RegenX-7'),
        ('nexus_core', 'Nexus CORE'),
        ('fermi_iii', 'Fermi-III'),
        ('helios_fusiondrive', 'Helios FusionDrive'),
        ('atucha_qtronix', 'Atucha Q-Tronix'),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=50, choices=REACTOR_CHOICES, unique=True)
    type = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField(default=0)

    annual_roi_rate = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        help_text="Annual ROI as decimal, can be negative (ex: 0.0650 = 6.5%)"
    )

    carbon_offset_tonnes_co2_per_nuc_per_year = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0000'))],
        help_text="Tonnes of CO₂ offset per $NUC invested per year"
    )

    total_funding_needed = models.DecimalField(
    max_digits=15, 
    decimal_places=2,
    help_text="Total $NUC needed to fully fund this reactor"
    )

    current_funding = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=Decimal('0.00'),
        help_text="Total $NUC currently invested in this reactor"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Nuclear Reactor"
        verbose_name_plural = "Nuclear Reactors"

    def __str__(self):
        return f"{self.name} ({self.location})"
    
    @property
    def funding_percentage(self):
        """Calculate percentage of total funding needed that's been invested"""
        if self.total_funding_needed == 0:
            return 0
        return round(float(self.current_funding / self.total_funding_needed * 100), 2)
    
    @property
    def available_funding(self):
        """Remaining funding capacity in $NUC"""
        return float(self.total_funding_needed) - float(self.current_funding)
    
    @property
    def is_fully_funded(self):
        """Check if reactor has reached full funding"""
        return self.current_funding >= self.total_funding_needed
    
    def can_invest(self, nuc_amount):
        """Check if a specific $NUC investment amount is valid"""
        return (
            self.is_active and
            nuc_amount > 0 and
            float(self.current_funding + nuc_amount) <= float(self.total_funding_needed)
        )
    
    def calculate_roi_projection(self, nuc_amount, years):
        """Calculate projected financial return for a given $NUC investment over time"""
        base_investment = float(nuc_amount)
        annual_return = base_investment * float(self.annual_roi_rate)
        total_return = annual_return * years
        return total_return
    
    def calculate_carbon_offset_projection(self, nuc_amount, years):
        """Calculate projected carbon offset in tonnes CO2 for a given $NUC investment"""
        return float(nuc_amount) * float(self.carbon_offset_tonnes_co2_per_nuc_per_year) * years