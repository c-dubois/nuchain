from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from apps.investments.models import Investment
from apps.reactors.models import Reactor


class InvestmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='investor',
            password='testpass123'
        )
        
        self.reactor = Reactor.objects.create(
            name='Test Reactor',
            slug='nuwave',
            type='SMR',
            description='Test reactor',
            location='Test Location',
            annual_roi_rate=Decimal('0.0450'),
            carbon_offset_tonnes_co2_per_nuc_per_year=Decimal('0.8500'),
            total_funding_needed=Decimal('180000')
        )
        
        self.investment = Investment.objects.create(
            user=self.user,
            reactor=self.reactor,
            amount_invested=Decimal('5000'),
        )
    
    def test_investment_creation(self):
        """Test investment is created with correct attributes"""
        self.assertEqual(self.investment.user, self.user)
        self.assertEqual(self.investment.reactor, self.reactor)
        self.assertEqual(self.investment.amount_invested, Decimal('5000'))
    
    def test_investment_str_representation(self):
        """Test string representation of investment"""
        expected = f"{self.user.username} → {self.reactor.name}: 5,000.00 $NUC invested"
        self.assertEqual(str(self.investment), expected)
    
    def test_investment_ordering(self):
        """Test investments are ordered by creation date (newest first)"""
        
        investment2 = Investment.objects.create(
            user=self.user,
            reactor=self.reactor,
            amount_invested=Decimal('3000'),
        )
        
        investments = Investment.objects.all()
        
        self.assertEqual(investments[0], investment2)
        self.assertEqual(investments[1], self.investment)
    
    def test_investment_cascading_delete_user(self):
        """Test that deleting user deletes their investments"""
        investment_id = self.investment.id
        self.user.delete()
        
        self.assertFalse(
            Investment.objects.filter(id=investment_id).exists()
        )
    
    def test_investment_cascading_delete_reactor(self):
        """Test that deleting reactor deletes related investments"""
        investment_id = self.investment.id
        self.reactor.delete()
        
        self.assertFalse(
            Investment.objects.filter(id=investment_id).exists()
        )
