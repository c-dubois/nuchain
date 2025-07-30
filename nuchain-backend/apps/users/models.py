from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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
        default=Decimal('25000.00'),
        help_text="User's balance in $NUC"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Balance: {self.balance:,.2f} $NUC"
    
    def can_afford(self, amount):
        """Check if user can afford an investment"""
        return self.balance >= amount
    
    def deduct_balance(self, amount):
        """Deduct investment amount from balance"""
        if self.can_afford(amount):
            self.balance -= amount
            self.save()
            return True
        return False
    
    @transaction.atomic
    def reset_wallet(self):
        """
        Reset wallet to starting balance of 25,000 $NUC.
        Clear all investments associated with user and reactor's current investments.
        """
        
        user_investments = self.user.investments.all()
        for investment in user_investments:
            reactor = investment.reactor
            reactor.current_funding -= investment.amount_invested
            reactor.save()

        user_investments.delete()

        self.balance = Decimal('25000.00')
        self.save()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if hasattr(instance, 'profile'):
            instance.profile.save()



