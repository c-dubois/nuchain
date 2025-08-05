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
    
    def test_successful_registration(self):
        """Test successful user registration"""
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
        self.assertEqual(response.data['user']['username'], 'newuser')
        self.assertEqual(response.data['user']['balance'], 25000.0)
        self.assertIn('25,000 $NUC tokens', response.data['message'])

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
        self.client.force_authenticate(user=self.user)
        self.reset_url = reverse('reset-wallet')

    def test_reset_wallet(self):
        """Test wallet reset functionality"""
        # First reduce balance
        self.user.profile.deduct_balance(Decimal('10000'))
        self.assertEqual(self.user.profile.balance, Decimal('15000'))
        
        # Reset wallet
        response = self.client.post(self.reset_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], 25000.0)
        self.assertIn('Wallet reset successfully', response.data['message'])
        
        # Verify in database
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.balance, Decimal('25000'))

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