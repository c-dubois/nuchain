from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from decimal import Decimal
from apps.investments.models import Investment
from apps.investments.serializers import (
    InvestmentSerializer,
    CreateInvestmentSerializer,
    PortfolioSummarySerializer
)
from apps.reactors.models import Reactor


class InvestmentSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.reactor = Reactor.objects.create(
            name='Test Reactor',
            slug='nuwave',
            type='SMR',
            description='Test',
            location='Test Location',
            annual_roi_rate=Decimal('0.0450'),
            carbon_offset_tonnes_co2_per_nuc_per_year=Decimal('0.8500'),
            total_funding_needed=Decimal('180000')
        )
        
        self.investment = Investment.objects.create(
            user=self.user,
            reactor=self.reactor,
            amount_invested=Decimal('5000'),
            time_period_years=5
        )
    
    def test_investment_serializer_fields(self):
        """Test InvestmentSerializer returns correct fields"""
        serializer = InvestmentSerializer(self.investment)
        data = serializer.data
        
        self.assertIn('id', data)
        self.assertIn('user', data)
        self.assertIn('reactor', data)
        self.assertIn('amount_invested', data)
        self.assertIn('created_at', data)
        
        # Check nested reactor data
        self.assertIsInstance(data['reactor'], dict)
        self.assertEqual(data['reactor']['name'], 'Test Reactor')
    
    def test_user_field_string_representation(self):
        """Test user field shows username"""
        serializer = InvestmentSerializer(self.investment)
        self.assertEqual(serializer.data['user'], 'testuser')


class CreateInvestmentSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.reactor = Reactor.objects.create(
            name='Test Reactor',
            slug='nuwave',
            type='SMR',
            description='Test',
            location='Test Location',
            annual_roi_rate=Decimal('0.0450'),
            carbon_offset_tonnes_co2_per_nuc_per_year=Decimal('0.8500'),
            total_funding_needed=Decimal('180000'),
            current_funding=Decimal('0')
        )
        
        # Create request context
        request = self.factory.post('/')
        request.user = self.user
        self.context = {'request': request}
    
    def test_valid_investment_data(self):
        """Test serializer with valid investment data"""
        data = {
            'reactor_id': self.reactor.id,
            'amount_invested': '10000'
        }
        
        serializer = CreateInvestmentSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        
        # Check validated data includes reactor object
        self.assertIn('reactor', serializer.validated_data)
        self.assertEqual(serializer.validated_data['reactor'], self.reactor)
    
    def test_invalid_reactor_id(self):
        """Test serializer with non-existent reactor"""
        data = {
            'reactor_id': 9999,
            'amount_invested': '1000'
        }
        
        serializer = CreateInvestmentSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Reactor not found', str(serializer.errors))
    
    def test_insufficient_user_balance(self):
        """Test serializer when user has insufficient balance"""
        data = {
            'reactor_id': self.reactor.id,
            'amount_invested': '30000'  # More than default 25,000
        }
        
        serializer = CreateInvestmentSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Insufficient balance', str(serializer.errors))
    
    def test_exceeds_reactor_capacity(self):
        """Test when investment exceeds reactor capacity"""
        self.reactor.current_funding = Decimal('179500')
        self.reactor.save()
        
        data = {
            'reactor_id': self.reactor.id,
            'amount_invested': '1000'  # Would put it over capacity
        }
        
        serializer = CreateInvestmentSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Cannot invest', str(serializer.errors))


class PortfolioSummarySerializerTest(TestCase):
    def test_portfolio_summary_serializer(self):
        """Test PortfolioSummarySerializer with complete data"""
        data = {
            'total_invested': Decimal('50000'),
            'investment_count': 3,
            'reactors_invested_in': ['Reactor 1', 'Reactor 2'],
            'projections': [
                {
                    'time_period_years': 1,
                    'total_roi': Decimal('2250'),
                    'total_carbon_offset': Decimal('42.5'),
                    'total_return': Decimal('52250'),
                    'roi_percentage': Decimal('4.5')
                },
                {
                    'time_period_years': 5,
                    'total_roi': Decimal('11250'),
                    'total_carbon_offset': Decimal('212.5'),
                    'total_return': Decimal('61250'),
                    'roi_percentage': Decimal('22.5')
                }
            ]
        }
        
        serializer = PortfolioSummarySerializer(data)
        serialized_data = serializer.data
        
        self.assertEqual(serialized_data['total_invested'], '50000.00')
        self.assertEqual(serialized_data['investment_count'], 3)
        self.assertEqual(len(serialized_data['reactors_invested_in']), 2)
        self.assertEqual(len(serialized_data['projections']), 2)
        
        # Check projection data
        first_projection = serialized_data['projections'][0]
        self.assertEqual(first_projection['time_period_years'], 1)
        self.assertEqual(first_projection['total_roi'], '2250.00')
        self.assertEqual(first_projection['roi_percentage'], '4.50')