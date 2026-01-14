from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from decimal import Decimal
from apps.reactors.models import Reactor


class InvestmentIntegrationTest(TestCase):
    """Integration tests for the complete investment flow"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create reactors
        self.reactor1 = Reactor.objects.create(
            name='NuWave',
            slug='nuwave',
            type='SMR',
            description='Test reactor 1',
            location='USA',
            annual_roi_rate=Decimal('0.0450'),
            carbon_offset_tonnes_co2_per_nuc_per_year=Decimal('0.8500'),
            total_funding_needed=Decimal('180000')
        )
        
        self.reactor2 = Reactor.objects.create(
            name='Phoenix',
            slug='phoenix_regenx7',
            type='MSR',
            description='Test reactor 2',
            location='France',
            annual_roi_rate=Decimal('0.0680'),
            carbon_offset_tonnes_co2_per_nuc_per_year=Decimal('1.1500'),
            total_funding_needed=Decimal('150000')
        )
    
    @patch('apps.users.views.BlockchainService')
    @patch('apps.investments.views.BlockchainService')
    def test_complete_investment_flow(self, mock_investment_blockchain, mock_user_blockchain):
        """Test complete user journey from registration to investment"""
        # Setup user blockchain mock (for registration and reset)
        mock_user_service = MagicMock()
        mock_user_service.mint_signup.return_value = (
            '0x1234567890abcdef1234567890abcdef12345678',
            '0xmint_tx_hash'
        )
        mock_user_service.reset_portfolio.return_value = '0xreset_tx_hash'
        mock_user_blockchain.return_value = mock_user_service
        
        # Setup investment blockchain mock
        mock_invest_service = MagicMock()
        mock_invest_service.lock_tokens.return_value = '0xlock_tx_hash'
        mock_invest_service.get_balance.return_value = Decimal('25000')
        mock_invest_service.get_locked_balance.return_value = Decimal('15000')
        mock_invest_service.get_available_balance.return_value = Decimal('10000')
        mock_investment_blockchain.return_value = mock_invest_service
        
        # 1. Register a new user
        register_data = {
            'username': 'investor1',
            'email': 'investor1@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123',
            'first_name': 'Test',
            'last_name': 'Investor'
        }
        response = self.client.post(reverse('register'), register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('wallet', response.data)
        
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # 2. Check initial balance
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], '25000.00')
        
        # 3. View available reactors
        response = self.client.get(reverse('reactor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # 4. Make first investment
        investment_data = {
            'reactor_id': self.reactor1.id,
            'amount_invested': '10000'
        }
        response = self.client.post(reverse('investment-list'), investment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['amount_invested'], 10000.0)
        self.assertEqual(response.data['remaining_balance'], 15000.0)
        self.assertIn('tx_hash', response.data)
        
        # 5. Make second investment
        investment_data2 = {
            'reactor_id': self.reactor2.id,
            'amount_invested': '5000'
        }
        response = self.client.post(reverse('investment-list'), investment_data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['remaining_balance'], 10000.0)
        
        # 6. Check portfolio summary
        response = self.client.get(reverse('investment-portfolio-summary'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_invested'], '15000.00')
        self.assertEqual(response.data['investment_count'], 2)
        self.assertEqual(len(response.data['reactors_invested_in']), 2)
        self.assertIn('wallet', response.data)
        
        # 7. Verify projections
        projections = response.data['projections']
        self.assertEqual(len(projections), 4)  # 1, 2, 5, 10 years
        
        # Verify 1-year projection calculations
        one_year = projections[0]
        expected_roi = (
            Decimal('10000') * Decimal('0.0450') +  # NuWave
            Decimal('5000') * Decimal('0.0680')     # Phoenix
        )
        self.assertEqual(Decimal(one_year['total_roi']), expected_roi)
        
        # 8. Reset wallet - update mock for reset
        mock_invest_service.get_locked_balance.return_value = Decimal('0')
        mock_invest_service.get_available_balance.return_value = Decimal('25000')
        
        response = self.client.post(reverse('reset-wallet'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], 25000.0)
        self.assertIn('tx_hash', response.data)
        
        # 9. Verify investments are cleared
        response = self.client.get(reverse('investment-list'))
        self.assertEqual(len(response.data['results']), 0)
        
        # 10. Verify reactor funding was reset
        self.reactor1.refresh_from_db()
        self.reactor2.refresh_from_db()
        self.assertEqual(self.reactor1.current_funding, Decimal('0'))
        self.assertEqual(self.reactor2.current_funding, Decimal('0'))
    
    @patch('apps.users.views.BlockchainService')
    @patch('apps.investments.views.BlockchainService')
    def test_multiple_users_investing_in_same_reactor(self, mock_investment_blockchain, mock_user_blockchain):
        """Test multiple users investing in the same reactor"""
        # Setup mocks
        mock_user_service = MagicMock()
        wallet_counter = [0]
        def mock_mint():
            wallet_counter[0] += 1
            return (f'0x{wallet_counter[0]:040d}', f'0xtx{wallet_counter[0]}')
        mock_user_service.mint_signup.side_effect = mock_mint
        mock_user_blockchain.return_value = mock_user_service
        
        mock_invest_service = MagicMock()
        mock_invest_service.lock_tokens.return_value = '0xlock_tx_hash'
        mock_investment_blockchain.return_value = mock_invest_service

        def register_and_authenticate(username):
            register_data = {
                'username': username,
                'email': f'{username}@example.com',
                'password': 'pass12345',
                'password_confirm': 'pass12345',
                'first_name': 'Test',
                'last_name': 'User'
            }
            response = self.client.post(reverse('register'), register_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            access_token = response.data['access']
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # User 1 invests
        register_and_authenticate('user1')
        response = self.client.post(
            reverse('investment-list'),
            {'reactor_id': self.reactor1.id, 'amount_invested': '5000'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # User 2 invests
        register_and_authenticate('user2')
        response = self.client.post(
            reverse('investment-list'),
            {'reactor_id': self.reactor1.id, 'amount_invested': '2500'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify reactor funding
        self.reactor1.refresh_from_db()
        self.assertEqual(self.reactor1.current_funding, Decimal('7500'))
        
        # Verify each user sees only their investments
        response = self.client.get(reverse('investment-list'))
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['amount_invested'], '2500.00')
    
    @patch('apps.investments.views.BlockchainService')
    def test_reactor_capacity_limits(self, mock_blockchain_class):
        """Test that reactor capacity limits are enforced across users"""
        mock_service = MagicMock()
        mock_service.lock_tokens.return_value = '0xlock_tx_hash'
        mock_blockchain_class.return_value = mock_service
        
        # Set reactor close to capacity
        self.reactor1.current_funding = Decimal('179000')
        self.reactor1.save()
        
        user = User.objects.create_user(
            username='testuser',
            password='pass123'
        )
        user.profile.wallet_address = '0x1234567890abcdef1234567890abcdef12345678'
        user.profile.save()
        
        self.client.force_authenticate(user=user)
        
        # Try to invest more than available capacity
        response = self.client.post(
            reverse('investment-list'),
            {'reactor_id': self.reactor1.id, 'amount_invested': '2000'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Cannot invest', str(response.data))
        
        # Invest exactly the available amount
        response = self.client.post(
            reverse('investment-list'),
            {'reactor_id': self.reactor1.id, 'amount_invested': '1000'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify reactor is now fully funded
        self.reactor1.refresh_from_db()
        self.assertTrue(self.reactor1.is_fully_funded)