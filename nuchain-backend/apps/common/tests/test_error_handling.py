from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User


class ErrorHandlingTest(TestCase):
    """Test error handling across the application"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_404_for_nonexistent_resources(self):
        """Test 404 responses for non-existent resources"""
        # Non-existent reactor
        response = self.client.get(
            reverse('reactor-detail', kwargs={'pk': 9999})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Non-existent investment
        response = self.client.get(
            reverse('investment-detail', kwargs={'pk': 9999})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_invalid_data_types(self):
        """Test handling of invalid data types"""
        # String instead of number for amount
        response = self.client.post(
            reverse('investment-list'),
            {'reactor_id': 1, 'amount_invested': 'not-a-number'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Negative amount
        response = self.client.post(
            reverse('investment-list'),
            {'reactor_id': 1, 'amount_invested': '-1000'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_missing_required_fields(self):
        """Test handling of missing required fields"""
        # Missing reactor_id
        response = self.client.post(
            reverse('investment-list'),
            {'amount_invested': '1000'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('reactor_id', response.data)
        
        # Missing amount_invested
        response = self.client.post(
            reverse('investment-list'),
            {'reactor_id': 1},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount_invested', response.data)