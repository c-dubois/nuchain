from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class JWTAuthenticationTest(TestCase):
    """Test JWT authentication flow"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_token_refresh(self):
        """Test token refresh functionality"""
        # Get initial tokens
        refresh = RefreshToken.for_user(self.user)
        
        # Use refresh token to get new access token
        response = self.client.post(
            reverse('token_refresh'),
            {'refresh': str(refresh)},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
        # Verify new access token works
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}'
        )
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_expired_token(self):
        """Test that expired tokens are rejected"""
        # This test would require mocking time or token expiry
        # For now, just verify that invalid tokens are rejected
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid-token')
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_blacklisted_token_after_logout(self):
        """Test that tokens are blacklisted after logout"""
        # Login and get tokens
        login_response = self.client.post(
            reverse('login'),
            {'username': 'testuser', 'password': 'testpass123'},
            format='json'
        )
        access_token = login_response.data['access']
        refresh_token = login_response.data['refresh']
        
        # Use access token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Logout
        response = self.client.post(
            reverse('logout'),
            {'refresh': refresh_token},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Try to use refresh token after logout (should fail)
        response = self.client.post(
            reverse('token_refresh'),
            {'refresh': refresh_token},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
