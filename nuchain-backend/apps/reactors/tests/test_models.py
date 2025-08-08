from django.test import TestCase
from decimal import Decimal
from apps.reactors.models import Reactor

class ReactorModelTest(TestCase):
    def setUp(self):
        self.reactor = Reactor.objects.create(
            name='Test Reactor',
            slug='testreactor',
            type='SMR',
            description='Test reactor description',
            location='Test Location',
            annual_roi_rate=Decimal('0.0450'),
            carbon_offset_tonnes_co2_per_nuc_per_year=Decimal('0.8500'),
            total_funding_needed=Decimal('180000'),
            current_funding=Decimal('50000'),
        )

    def test_reactor_creation(self):
        """Test reactor is created with correct attributes"""
        self.assertEqual(self.reactor.name, 'Test Reactor')
        self.assertEqual(self.reactor.slug, 'testreactor')
        self.assertEqual(self.reactor.annual_roi_rate, Decimal('0.0450'))
        self.assertTrue(self.reactor.is_active)

    def test_funding_percentage(self):
        """Test funding percentage calculation"""
        expected_percentage = (50000 / 180000) * 100
        self.assertAlmostEqual(
            self.reactor.funding_percentage,
            expected_percentage,
            places=2
        )

    def test_available_funding(self):
        """Test available funding calculation"""
        expected_available = 180000 - 50000
        self.assertEqual(self.reactor.available_funding, expected_available)
    
    def test_is_fully_funded(self):
        """Test fully funded check"""
        self.assertFalse(self.reactor.is_fully_funded)
        
        # Set current funding to total needed
        self.reactor.current_funding = self.reactor.total_funding_needed
        self.reactor.save()
        
        self.assertTrue(self.reactor.is_fully_funded)
    
    def test_can_invest(self):
        """Test investment validation"""
        # Valid investment
        self.assertTrue(self.reactor.can_invest(Decimal('10000')))
        
        # Investment exceeding capacity
        self.assertFalse(self.reactor.can_invest(Decimal('140000')))
        
        # Negative investment
        self.assertFalse(self.reactor.can_invest(Decimal('-1000')))
        
        # Inactive reactor
        self.reactor.is_active = False
        self.assertFalse(self.reactor.can_invest(Decimal('1000')))
    
    def test_calculate_roi_projection(self):
        """Test ROI calculation"""
        investment = Decimal('10000')
        years = 5
        
        expected_roi = float(investment) * float(self.reactor.annual_roi_rate) * years
        calculated_roi = self.reactor.calculate_roi_projection(investment, years)
        
        self.assertAlmostEqual(calculated_roi, expected_roi, places=2)
    
    def test_calculate_carbon_offset_projection(self):
        """Test carbon offset calculation"""
        investment = Decimal('10000')
        years = 5
        
        expected_offset = (
            float(investment) * 
            float(self.reactor.carbon_offset_tonnes_co2_per_nuc_per_year) * 
            years
        )
        calculated_offset = self.reactor.calculate_carbon_offset_projection(
            investment, years
        )
        
        self.assertAlmostEqual(calculated_offset, expected_offset, places=4)
    
    def test_str_representation(self):
        """Test string representation"""
        expected_str = f"{self.reactor.name} ({self.reactor.location})"
        self.assertEqual(str(self.reactor), expected_str)
    
    def test_negative_roi_rate(self):
        """Test reactor with negative ROI (like Helios FusionDrive)"""
        reactor = Reactor.objects.create(
            name='Negative ROI Reactor',
            slug='helios_fusiondrive',
            type='Fusion',
            description='Test',
            location='Test',
            annual_roi_rate=Decimal('-0.0150'),
            carbon_offset_tonnes_co2_per_nuc_per_year=Decimal('3.1500'),
            total_funding_needed=Decimal('95000')
        )
        
        roi = reactor.calculate_roi_projection(Decimal('10000'), 5)
        self.assertLess(roi, 0)