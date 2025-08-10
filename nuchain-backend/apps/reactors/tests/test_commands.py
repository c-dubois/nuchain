from django.test import TestCase
from django.core.management import call_command
from io import StringIO
from apps.reactors.models import Reactor
from decimal import Decimal


class CreateReactorsCommandTest(TestCase):
    def test_create_reactors_command(self):
        """Test the create_reactors management command"""
        out = StringIO()
        call_command('create_reactors', stdout=out)

        # Check that all 6 reactors were created
        self.assertEqual(Reactor.objects.count(), 6)

        # Check specific reactors exist
        reactor_slugs = [
            'nuwave',
            'phoenix_regenx7',
            'nexus_core',
            'fermi_iii',
            'helios_fusiondrive',
            'atucha_qtronix'
        ]
        
        for slug in reactor_slugs:
            self.assertTrue(
                Reactor.objects.filter(slug=slug).exists(),
                f"Reactor with slug '{slug}' should exist"
            )
        
        # Verify specific reactor details
        nuwave = Reactor.objects.get(slug='nuwave')
        self.assertEqual(nuwave.name, 'NuWave')
        self.assertEqual(nuwave.location, 'Cascadia Basin, Washington, USA')
        self.assertEqual(nuwave.annual_roi_rate, Decimal('0.0450'))
        
        # Check output messages
        output = out.getvalue()
        self.assertIn('Successfully created reactor', output)
    
    def test_create_reactors_command_idempotent(self):
        """Test that running command twice doesn't create duplicates"""
        # Run command first time
        call_command('create_reactors')
        self.assertEqual(Reactor.objects.count(), 6)
        
        # Run command second time
        out = StringIO()
        call_command('create_reactors', stdout=out)

        # Should still have only 6 reactors
        self.assertEqual(Reactor.objects.count(), 6)
        
        # Check output shows reactors already exist
        output = out.getvalue()
        self.assertIn('Successfully updated reactor', output)
        self.assertNotIn('Successfully created reactor', output)

    def test_reactor_data_integrity(self):
        """Test that all reactor data is correctly loaded"""
        call_command('create_reactors')
        
        # Test each reactor's key attributes
        test_cases = [
            {
                'slug': 'nuwave',
                'total_funding': Decimal('180000'),
                'roi_rate': Decimal('0.0450'),
                'carbon_offset': Decimal('0.8500')
            },
            {
                'slug': 'phoenix_regenx7',
                'total_funding': Decimal('150000'),
                'roi_rate': Decimal('0.0680'),
                'carbon_offset': Decimal('1.1500')
            },
            {
                'slug': 'helios_fusiondrive',
                'total_funding': Decimal('95000'),
                'roi_rate': Decimal('-0.0150'), 
                'carbon_offset': Decimal('3.1500')
            }
        ]
        
        for test_case in test_cases:
            reactor = Reactor.objects.get(slug=test_case['slug'])
            self.assertEqual(
                reactor.total_funding_needed,
                test_case['total_funding']
            )
            self.assertEqual(
                reactor.annual_roi_rate,
                test_case['roi_rate']
            )
            self.assertEqual(
                reactor.carbon_offset_tonnes_co2_per_nuc_per_year,
                test_case['carbon_offset']
            )