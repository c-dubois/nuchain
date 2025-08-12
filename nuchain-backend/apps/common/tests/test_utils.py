"""Test utility functions and factories for all apps"""
from django.contrib.auth.models import User
from decimal import Decimal
from apps.reactors.models import Reactor
from apps.investments.models import Investment


class TestFactory:
    """Factory class for creating test objects"""
    
    @staticmethod
    def create_user(username='testuser', email='test@example.com', 
                   password='testpass123', balance=None, **kwargs):
        """Create a test user with profile"""
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **kwargs
        )
        if balance is not None:
            user.profile.balance = Decimal(str(balance))
            user.profile.save()
        return user
    
    @staticmethod
    def create_reactor(name='Test Reactor', slug='nuwave', 
                      total_funding=180000, current_funding=0, **kwargs):
        """Create a test reactor"""
        defaults = {
            'name': name,
            'slug': slug,
            'type': 'SMR',
            'description': 'Test reactor description',
            'location': 'Test Location',
            'annual_roi_rate': Decimal('0.0450'),
            'carbon_offset_tonnes_co2_per_nuc_per_year': Decimal('0.8500'),
            'total_funding_needed': Decimal(str(total_funding)),
            'current_funding': Decimal(str(current_funding)),
            'is_active': True
        }
        defaults.update(kwargs)
        return Reactor.objects.create(**defaults)
    
    @staticmethod
    def create_investment(user, reactor, amount=5000, **kwargs):
        """Create a test investment"""
        defaults = {
            'user': user,
            'reactor': reactor,
            'amount_invested': Decimal(str(amount)),
            'time_period_years': 5
        }
        defaults.update(kwargs)
        investment = Investment.objects.create(**defaults)
        
        # Update reactor funding
        reactor.current_funding += investment.amount_invested
        reactor.save()
        
        # Deduct from user balance
        user.profile.deduct_balance(investment.amount_invested)
        
        return investment