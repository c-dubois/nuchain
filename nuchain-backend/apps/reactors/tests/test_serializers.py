from django.test import TestCase
from decimal import Decimal
from apps.reactors.models import Reactor
from apps.reactors.serializers import ReactorSerializer

class ReactorSerializerTest(TestCase):
    def setUp(self):
        self.reactor = Reactor.objects.create(
            name='Test Reactor',
            slug='testreactor',
            type='SMR',
            description='Test description',
            location='Test Location',
            annual_roi_rate=Decimal('0.0450'),
            carbon_offset_tonnes_co2_per_nuc_per_year=Decimal('0.8500'),
            total_funding_needed=Decimal('180000'),
            current_funding=Decimal('50000'),
            image_url='https://example.com/test.jpg'
        )

    def test_serializer_fields(self):
        """Test that all expected fields are in serializer output"""
        serializer = ReactorSerializer(self.reactor)
        data = serializer.data
        
        expected_fields = [
            'id', 'name', 'slug', 'type', 'description', 'location',
            'annual_roi_rate', 'carbon_offset_tonnes_co2_per_nuc_per_year',
            'total_funding_needed', 'current_funding', 'funding_percentage',
            'available_funding', 'is_fully_funded', 'image_url', 'is_active',
            'created_at'
        ]
        
        for field in expected_fields:
            self.assertIn(field, data)
    
    def test_computed_fields(self):
        """Test that computed fields have correct values"""
        serializer = ReactorSerializer(self.reactor)
        data = serializer.data
        
        # Test funding_percentage
        expected_percentage = (50000 / 180000) * 100
        self.assertAlmostEqual(
            float(data['funding_percentage']),
            expected_percentage,
            places=2
        )
        
        # Test available_funding
        expected_available = 180000 - 50000
        self.assertEqual(float(data['available_funding']), expected_available)
        
        # Test is_fully_funded
        self.assertFalse(data['is_fully_funded'])
    
    def test_read_only_fields(self):
        """Test that computed fields are read-only"""
        serializer = ReactorSerializer(self.reactor)
        
        # Get field objects
        fields = serializer.fields
        
        # Check that computed fields are read-only
        self.assertTrue(fields['funding_percentage'].read_only)
        self.assertTrue(fields['available_funding'].read_only)
        self.assertTrue(fields['is_fully_funded'].read_only)