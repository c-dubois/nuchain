from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User


class PermissionTest(TestCase):
    """Test API permissions"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_unauthenticated_access_denied(self):
        """Test that unauthenticated requests are denied"""
        endpoints = [
            reverse('user-profile'),
            reverse('reactor-list'),
            reverse('investment-list'),
            reverse('investment-portfolio-summary'),
        ]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                f"Endpoint {endpoint} should require authentication"
            )
    
    def test_authenticated_access_allowed(self):
        """Test that authenticated requests are allowed"""
        self.client.force_authenticate(user=self.user)
        
        endpoints = [
            reverse('user-profile'),
            reverse('reactor-list'),
            reverse('investment-list'),
            reverse('investment-portfolio-summary'),
        ]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertNotEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                f"Endpoint {endpoint} should allow authenticated access"
            )
