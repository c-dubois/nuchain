from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal

class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
    
    @patch('apps.users.views.BlockchainService')
    def test_successful_registration(self, mock_blockchain_class):
        """Test successful user registration with blockchain wallet"""
        # Setup mock
        mock_service = MagicMock()
        mock_service.mint_signup.return_value = (
            '0x1234567890abcdef1234567890abcdef12345678',
            '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890'
        )
        mock_blockchain_class.return_value = mock_service
        
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'strongpass123',
            'password_confirm': 'strongpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertIn('wallet', response.data)
        self.assertEqual(response.data['user']['username'], 'newuser')
        self.assertEqual(response.data['user']['balance'], 25000.0)
        self.assertEqual(
            response.data['wallet']['address'],
            '0x1234567890abcdef1234567890abcdef12345678'
        )
        self.assertIn('25,000 $NUC tokens', response.data['message'])
        mock_service.mint_signup.assert_called_once()
    
    def test_registration_password_mismatch(self):
        """Test registration with mismatched passwords"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'strongpass123',
            'password_confirm': 'differentpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Passwords do not match', str(response.data))
    
    def test_registration_duplicate_username(self):
        """Test registration with existing username"""
        User.objects.create_user(username='existinguser', password='pass123')
        
        data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password': 'strongpass123',
            'password_confirm': 'strongpass123'
        }
        
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
    
    def test_registration_duplicate_email(self):
        """Test registration with existing email"""
        User.objects.create_user(
            username='user1',
            email='existing@example.com',
            password='pass123'
        )
        
        data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'strongpass123',
            'password_confirm': 'strongpass123'
        }
        
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

class UserLoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_successful_login(self):
        """Test successful login"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['message'], 'Login successful!')
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_nonexistent_user(self):
        """Test login with a non-existent user"""
        data = {
            'username': 'nonexistent',
            'password': 'somepassword'
        }
        
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserProfileTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client.force_authenticate(user=self.user)
        self.profile_url = reverse('user-profile')
        self.update_profile_url = reverse('update-profile')
    
    def test_get_profile_authenticated(self):
        """Test getting user profile when authenticated"""
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], '25000.00')
    
    def test_get_profile_unauthenticated(self):
        """Test getting user profile without authentication"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_profile(self):
        """Test updating user profile"""
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com'
        }
        
        response = self.client.put(self.update_profile_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Profile updated successfully')
        
        # Verify the update
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.email, 'updated@example.com')
    
    def test_update_profile_duplicate_email(self):
        """Test updating profile with email already in use"""
        User.objects.create_user(
            username='otheruser',
            email='taken@example.com',
            password='pass123'
        )
        
        data = {'email': 'taken@example.com'}
        
        response = self.client.put(self.update_profile_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

class WalletResetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Add wallet address to profile
        self.user.profile.wallet_address = '0x1234567890abcdef1234567890abcdef12345678'
        self.user.profile.save()
        
        self.client.force_authenticate(user=self.user)
        self.reset_url = reverse('reset-wallet')
    
    @patch('apps.users.views.BlockchainService')
    def test_reset_wallet(self, mock_blockchain_class):
        """Test wallet reset functionality with blockchain unlock"""
        mock_service = MagicMock()
        mock_service.reset_portfolio.return_value = '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890'
        mock_blockchain_class.return_value = mock_service
        
        # First reduce balance
        self.user.profile.deduct_balance(Decimal('10000'))
        self.assertEqual(self.user.profile.balance, Decimal('15000'))
        
        # Reset wallet
        response = self.client.post(self.reset_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], 25000.0)
        self.assertIn('Wallet reset successfully', response.data['message'])
        self.assertIn('tx_hash', response.data)
        self.assertIn('wallet', response.data)
        
        # Verify in database
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.balance, Decimal('25000'))
        mock_service.reset_portfolio.assert_called_once_with(
            '0x1234567890abcdef1234567890abcdef12345678'
        )
    
    def test_reset_wallet_no_wallet_address(self):
        """Test reset wallet fails when user has no wallet"""
        self.user.profile.wallet_address = None
        self.user.profile.save()
        
        response = self.client.post(self.reset_url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No wallet found', response.data['error'])

class ChangePasswordTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.change_password_url = reverse('change-password')
    
    def test_change_password_success(self):
        """Test successful password change"""
        data = {
            'old_password': 'testpass123',
            'new_password': 'newpass123',
            'new_password_confirm': 'newpass123'
        }
        
        response = self.client.post(self.change_password_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Password changed successfully')
        
        # Verify new password works
        self.client.logout()
        login_response = self.client.post(
            reverse('login'),
            {'username': 'testuser', 'password': 'newpass123'},
            format='json'
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

class LogoutTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.logout_url = reverse('logout')
    
    def test_logout_with_refresh_token(self):
        """Test logout with valid refresh token"""
        refresh = RefreshToken.for_user(self.user)
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(
            self.logout_url,
            {'refresh': str(refresh)},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logout successful')
    
    def test_logout_without_refresh_token(self):
        """Test logout without refresh token"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(self.logout_url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Refresh token required', response.data['error'])

class DeleteAccountTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.user.profile.wallet_address = '0x1234567890abcdef1234567890abcdef12345678'
        self.user.profile.save()
        
        self.client.force_authenticate(user=self.user)
        self.delete_account_url = reverse('delete-account')
    
    @patch('apps.users.views.BlockchainService')
    def test_delete_account(self, mock_blockchain_class):
        """Test account deletion with token burn"""
        mock_service = MagicMock()
        mock_service.burn_account.return_value = '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890'
        mock_blockchain_class.return_value = mock_service
        
        user_id = self.user.id
        
        response = self.client.delete(self.delete_account_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Account deleted successfully')
        self.assertIn('tx_hash', response.data)
        self.assertIn('tx_url', response.data)
        
        # Verify user deleted
        self.assertFalse(User.objects.filter(id=user_id).exists())
        mock_service.burn_account.assert_called_once()
    
    @patch('apps.users.views.BlockchainService')
    def test_delete_account_no_wallet(self, mock_blockchain_class):
        """Test account deletion when user has no wallet"""
        self.user.profile.wallet_address = None
        self.user.profile.save()
        
        user_id = self.user.id
        
        response = self.client.delete(self.delete_account_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('tx_hash', response.data)
        
        # Verify user still deleted
        self.assertFalse(User.objects.filter(id=user_id).exists())
        mock_blockchain_class.assert_not_called()