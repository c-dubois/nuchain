from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from decimal import Decimal
from apps.reactors.models import Reactor

class ReactorViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test reactors
        self.reactor1 = Reactor.objects.create(
            name='Reactor 1',
            slug='reactor1',
            type='SMR',
            description='Test reactor 1',
            location='Location 1',
            annual_roi_rate=Decimal('0.0450'),
            carbon_offset_tonnes_co2_per_nuc_per_year=Decimal('0.8500'),
            total_funding_needed=Decimal('180000'),
            is_active=True
        )
        
        self.reactor2 = Reactor.objects.create(
            name='Reactor 2',
            slug='reactor2',
            type='MSR',
            description='Test reactor 2',
            location='Location 2',
            annual_roi_rate=Decimal('0.0680'),
            carbon_offset_tonnes_co2_per_nuc_per_year=Decimal('1.1500'),
            total_funding_needed=Decimal('150000'),
            is_active=True
        )
        
        # Inactive reactor (should not appear in list)
        self.inactive_reactor = Reactor.objects.create(
            name='Inactive Reactor',
            slug='inactivereactor',
            type='HTGR',
            description='Inactive',
            location='Nowhere',
            annual_roi_rate=Decimal('0.0380'),
            carbon_offset_tonnes_co2_per_nuc_per_year=Decimal('1.4000'),
            total_funding_needed=Decimal('220000'),
            is_active=False
        )

    def test_list_reactors_authenticated(self):
        """Test listing reactors when authenticated"""
        self.client.force_authenticate(user=self.user)
        url = reverse('reactor-list')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Only active reactors
        
        # Check that inactive reactor is not in the list
        reactor_names = [r['name'] for r in response.data['results']]
        self.assertNotIn('Inactive Reactor', reactor_names)

    def test_list_reactors_unauthenticated(self):
        """Test listing reactors without authentication"""
        url = reverse('reactor-list')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_retrieve_reactor(self):
        """Test retrieving single reactor details"""
        self.client.force_authenticate(user=self.user)
        url = reverse('reactor-detail', kwargs={'pk': self.reactor1.pk})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Reactor 1')
        self.assertIn('funding_percentage', response.data)
        self.assertIn('available_funding', response.data)
        self.assertIn('is_fully_funded', response.data)
    
    def test_reactor_ordering(self):
        """Test that reactors are ordered by name"""
        self.client.force_authenticate(user=self.user)
        url = reverse('reactor-list')
        
        response = self.client.get(url)
        
        reactor_names = [r['name'] for r in response.data['results']]
        self.assertEqual(reactor_names, sorted(reactor_names))

    def test_reactor_read_only(self):
        """Test that reactor endpoints are read-only"""
        self.client.force_authenticate(user=self.user)
        url = reverse('reactor-detail', kwargs={'pk': self.reactor1.pk})
        
        # Try to update (should fail)
        response = self.client.put(url, {'name': 'Updated Name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Try to delete (should fail)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Try to create (should fail)
        list_url = reverse('reactor-list')
        response = self.client.post(list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
