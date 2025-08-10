from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from decimal import Decimal
from apps.investments.models import Investment
from apps.reactors.models import Reactor


class InvestmentViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create test users
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass123'
        )
        
        # Create test reactor
        self.reactor = Reactor.objects.create(
            name='Test Reactor',
            slug='nuwave',
            type='SMR',
            description='Test reactor',
            location='Test Location',
            annual_roi_rate=Decimal('0.0450'),
            carbon_offset_tonnes_co2_per_nuc_per_year=Decimal('0.8500'),
            total_funding_needed=Decimal('180000'),
            current_funding=Decimal('0')
        )
        
        # Create investment for user1
        self.investment = Investment.objects.create(
            user=self.user1,
            reactor=self.reactor,
            amount_invested=Decimal('5000'),
            time_period_years=5
        )
        
        # Update reactor funding
        self.reactor.current_funding = Decimal('5000')
        self.reactor.save()
        
        # Authenticate as user1
        self.client.force_authenticate(user=self.user1)
    
    def test_list_user_investments(self):
        """Test that users only see their own investments"""
        # Create investment for user2
        Investment.objects.create(
            user=self.user2,
            reactor=self.reactor,
            amount_invested=Decimal('3000'),
            time_period_years=2
        )
        
        url = reverse('investment-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['user'],
            self.user1.username
        )
    
    def test_create_investment_success(self):
        """Test successful investment creation"""
        url = reverse('investment-list')
        data = {
            'reactor_id': self.reactor.id,
            'amount_invested': '10000'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('investment', response.data)
        self.assertIn('Successfully invested', response.data['message'])
        self.assertEqual(response.data['amount_invested'], 10000.0)
        
        # Check reactor funding updated
        self.reactor.refresh_from_db()
        self.assertEqual(self.reactor.current_funding, Decimal('15000'))
        
        # Check user balance deducted
        self.user1.profile.refresh_from_db()
        self.assertEqual(self.user1.profile.balance, Decimal('15000'))
    
    def test_create_investment_insufficient_balance(self):
        """Test investment with insufficient balance"""
        url = reverse('investment-list')
        data = {
            'reactor_id': self.reactor.id,
            'amount_invested': '30000'  # More than user balance
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Insufficient balance', response.data['error'])
    
    def test_create_investment_exceeds_reactor_capacity(self):
        """Test investment exceeding reactor capacity"""
        # Set reactor close to capacity
        self.reactor.current_funding = Decimal('179000')
        self.reactor.save()
        
        url = reverse('investment-list')
        data = {
            'reactor_id': self.reactor.id,
            'amount_invested': '2000'  # Would exceed capacity
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Cannot invest', str(response.data))
    
    def test_create_investment_invalid_reactor(self):
        """Test investment with invalid reactor ID"""
        url = reverse('investment-list')
        data = {
            'reactor_id': 9999,
            'amount_invested': '1000'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_investment_inactive_reactor(self):
        """Test investment in inactive reactor"""
        self.reactor.is_active = False
        self.reactor.save()
        
        url = reverse('investment-list')
        data = {
            'reactor_id': self.reactor.id,
            'amount_invested': '1000'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_portfolio_summary_empty(self):
        """Test portfolio summary with no investments"""
        # Authenticate as user2 (no investments)
        self.client.force_authenticate(user=self.user2)
        
        url = reverse('investment-portfolio-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_invested'], 0)
        self.assertEqual(response.data['investment_count'], 0)
        self.assertEqual(len(response.data['reactors_invested_in']), 0)
        self.assertEqual(len(response.data['projections']), 0)
    
    def test_portfolio_summary_with_investments(self):
        """Test portfolio summary with investments"""
        # Create another reactor and investment
        reactor2 = Reactor.objects.create(
            name='Reactor 2',
            slug='phoenix_regenx7',
            type='MSR',
            description='Test',
            location='Location 2',
            annual_roi_rate=Decimal('0.0680'),
            carbon_offset_tonnes_co2_per_nuc_per_year=Decimal('1.1500'),
            total_funding_needed=Decimal('150000')
        )
        
        Investment.objects.create(
            user=self.user1,
            reactor=reactor2,
            amount_invested=Decimal('8000'),
            time_period_years=10
        )
        
        url = reverse('investment-portfolio-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_invested'], '13000.00')
        self.assertEqual(response.data['investment_count'], 2)
        self.assertEqual(len(response.data['reactors_invested_in']), 2)
        
        # Check projections
        self.assertEqual(len(response.data['projections']), 4)  # 1, 2, 5, 10 years
        
        # Verify first projection (1 year)
        projection_1yr = response.data['projections'][0]
        self.assertEqual(projection_1yr['time_period_years'], 1)
        
        # Calculate expected ROI for 1 year
        expected_roi = (
            Decimal('5000') * Decimal('0.0450') +  # Reactor 1
            Decimal('8000') * Decimal('0.0680')     # Reactor 2
        )
        self.assertEqual(
            Decimal(projection_1yr['total_roi']),
            expected_roi
        )
    
    def test_investment_authentication_required(self):
        """Test that authentication is required for all endpoints"""
        self.client.force_authenticate(user=None)
        
        # Test list
        response = self.client.get(reverse('investment-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test create
        response = self.client.post(reverse('investment-list'), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test portfolio summary
        response = self.client.get(reverse('investment-portfolio-summary'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)