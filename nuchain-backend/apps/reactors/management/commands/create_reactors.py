from django.core.management.base import BaseCommand
from apps.reactors.models import Reactor
from decimal import Decimal

class Command(BaseCommand):
    help = "Create and initialize 5 fictional nuclear reactors"

    def handle(self, *args, **options):
        reactors_data = [
            {
                'name': 'NuWave',
                'slug': 'nuwave',
                'type': 'Pressurized Water Small Modular Reactor (SMR)',
                'description': 'The NuWave SMR is a state-of-the-art light water reactor built on modular, factory-fabricated design principles. Optimized for deployment in distributed grids, remote regions, or developing nations, NuWave offers passive safety, underground installation, and rapid deployment. Its core is designed for 20-year sealed operation with no on-site refueling and integrated desalination and hydrogen co-generation options.',
                'location': 'Cascadia Basin, Washington, USA',
                'annual_roi_rate': Decimal('0.0450'),
                'carbon_offset_tonnes_co2_per_nuc_per_year': Decimal('0.8500'),
                'total_funding_needed': 180000,
                'display_order': 1
            },
            {
                'name': 'Helios FusionDrive',
                'slug': 'helios_fusiondrive',
                'type': 'Hybrid Fusion-Fission Blanket Reactor',
                'description': 'Helios FusionDrive is a cutting-edge hybrid reactor using deuterium-tritium magnetic fusion as a neutron source to activate a subcritical fission blanket composed of thorium or depleted uranium. This architecture allows Helios to extract energy from otherwise inert materials, generate new fuel, and transmute nuclear waste—all while remaining inherently safe due to its reliance on externally driven neutronics. The first grid-integrated pilot was developed under a public–private partnership as part of an international effort to commercialize fusion energy by the 2040s.',
                'location': 'Tokamak Research, Kagoshima Prefecture, Japan',
                'annual_roi_rate': Decimal('-0.0150'),
                'carbon_offset_tonnes_co2_per_nuc_per_year': Decimal('3.1500'),
                'total_funding_needed': 95000,
                'display_order': 2
            },
            {
                'name': 'Phoenix RegenX-7',
                'slug': 'phoenix_regenx7',
                'type': 'Next-Gen Molten Salt Reactor (MSR)',
                'description': 'The Phoenix RegenX-7 is a fluoride-based molten salt reactor operating at atmospheric pressure with passive convection cooling and intrinsic fuel recycling. It uses liquid thorium fuel, enabling in-core breeding of U-233 and near-zero long-lived waste production. Phoenix’s RegenX system allows real-time isotopic rebalancing and automated online fission product removal, giving it a uniquely long continuous operation lifespan.',
                'location': 'La Drôme Nucléaire, Normandy, France',
                'annual_roi_rate': Decimal('0.0680'),
                'carbon_offset_tonnes_co2_per_nuc_per_year': Decimal('1.15000'),
                'total_funding_needed': 150000,
                'display_order': 3
            },
            {
                'name': 'Fermi-III',
                'slug': 'fermi_iii',
                'type': 'Lead-Cooled Fast Breeder Reactor (LCFBR)',
                'description': 'Fermi-III is a Generation IV fast-spectrum reactor designed for long-term, high-efficiency energy production using recycled nuclear fuel and depleted uranium. Building on decades of breeder reactor research, Fermi-III uses molten lead coolant for its superior thermal capacity and radiation shielding. With an embedded fuel recycling loop, it dramatically reduces the volume and half-life of nuclear waste, making it an ideal component of closed fuel-cycle strategies. Fermi-III is engineered for grid-scale deployment in countries pursuing next-gen nuclear as a pillar of long-term energy sovereignty.',
                'location': 'Cobalt Energy Complex, Ontario, Canada',
                'annual_roi_rate': Decimal('0.0220'),
                'carbon_offset_tonnes_co2_per_nuc_per_year': Decimal('1.8500'),
                'total_funding_needed': 160000,
                'display_order': 4
            },
            {
                'name': 'Atucha Q-Tronix',
                'slug': 'atucha_qtronix',
                'type': 'Quantum-Assisted Traveling Wave Reactor (QTWR)',
                'description': 'Atucha Q-Tronix is a next-generation Quantum-Assisted Traveling Wave Reactor, developed for ultra-long-lifecycle energy production using depleted uranium and in-core breeding of fissile fuel. What sets Atucha Q-Tronix apart is its integration with a quantum computing co-processor that optimizes neutron flux propagation, reactor core migration, and adaptive burn-up zones in real time. Located in the Mendoza Energy Frontier, Argentina, this reactor operates with minimal refueling over decades, enabling stable, high-efficiency energy in regions with limited nuclear fuel infrastructure. Atucha Q-Tronix represents a leap forward in predictive reactor control and fuel utilization for developing markets.',
                'location': 'Frontera Energética del Sur, Mendoza, Argentina',
                'annual_roi_rate': Decimal('0.0420'),
                'carbon_offset_tonnes_co2_per_nuc_per_year': Decimal('1.6000'),
                'total_funding_needed': 175000,
                'display_order': 5
            },
            {
                'name': 'Nexus CORE',
                'slug': 'nexus_core',
                'type': 'High-Temperature Gas-Cooled Reactor (HTGR)',
                'description': 'The Nexus CORE (Cognitive Optimized Reactor Environment) uses pebble-bed TRISO fuel in a helium-cooled reactor, enabling extremely high outlet temperatures for industrial heat, hydrogen production, and efficient power generation. A networked AI system manages thermal loads, predictive maintenance, and demand forecasting across a fleet of reactors. CORE modules can be linked to form a "neural reactor network" for mega-scale power coordination in decentralized grids or heavy industrial zones where heat and power co-generation are critical.',
                'location': 'NeueTech District, Hamburg, Germany',
                'annual_roi_rate': Decimal('0.0380'),
                'carbon_offset_tonnes_co2_per_nuc_per_year': Decimal('1.4000'),
                'total_funding_needed': 220000,
                'display_order': 6
            }
        ]

        for reactor_data in reactors_data:
            reactor, created = Reactor.objects.get_or_create(
                slug=reactor_data['slug'],
                defaults=reactor_data
            )
            if not created:
                for field, value in reactor_data.items():
                    setattr(reactor, field, value)
                reactor.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully updated reactor "{reactor.name}"')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created reactor "{reactor.name}"')
                )

        self.stdout.write(
            self.style.SUCCESS('All reactors have been processed!')
        )