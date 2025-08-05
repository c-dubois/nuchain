from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from apps.users.models import UserProfile

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_profile_created_on_user_creation(self):
        """Test that a UserProfile is automatically created when a User is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)

    def test_default_balance(self):
        """Test that new users start with 25,000 $NUC"""
        self.assertEqual(self.user.profile.balance, Decimal('25000.00'))

    def test_can_afford_method(self):
        """Test can_afford method"""
        self.assertTrue(self.user.profile.can_afford(Decimal('1000')))
        self.assertTrue(self.user.profile.can_afford(Decimal('25000')))
        self.assertFalse(self.user.profile.can_afford(Decimal('25000.01')))

    def test_deduct_balance_successful(self):
        """Test successful balance deduction"""
        initial_balance = self.user.profile.balance
        deduction_amount = Decimal('5000')

        result = self.user.profile.deduct_balance(deduction_amount)

        self.assertTrue(result)
        self.assertEqual(self.user.profile.balance, initial_balance - deduction_amount)

    def test_deduct_balance_insufficient_funds(self):
        """Test balance deduction fails when insufficient funds"""
        initial_balance = self.user.profile.balance
        deduction_amount = Decimal('30000')

        result = self.user.profile.deduct_balance(deduction_amount)

        self.assertFalse(result)
        self.assertEqual(self.user.profile.balance, initial_balance)

    def test_reset_wallet(self):
        """Test resetting wallet to starting balance"""
        # First deduct some balance
        self.user.profile.deduct_balance(Decimal('10000'))
        self.assertEqual(self.user.profile.balance, Decimal('15000'))
        
        # Reset wallet
        self.user.profile.reset_wallet()
        
        # Check balance reset to 25,000 $NUC
        self.assertEqual(self.user.profile.balance, Decimal('25000.00'))

    def test_str_representation(self):
        """Test string representation of UserProfile"""
        expected_str = f"{self.user.username} - Balance: 25,000.00 $NUC"
        self.assertEqual(str(self.user.profile), expected_str)