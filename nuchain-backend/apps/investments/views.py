from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.db import transaction
from decimal import Decimal
from .models import Investment
from .serializers import (
    InvestmentSerializer,
    CreateInvestmentSerializer,
    PortfolioSummarySerializer
)
from apps.blockchain.services import BlockchainService
from apps.blockchain.exceptions import BlockchainError

class InvestmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing investments
    """
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return investments for the current user only"""
        return Investment.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Use difference serializers for different actions"""
        if self.action == 'create':
            return CreateInvestmentSerializer
        return InvestmentSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create a new investment and lock tokens on blockchain"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            reactor = serializer.validated_data['reactor']
            amount = serializer.validated_data['amount_invested']
            wallet_address = request.user.profile.wallet_address
            
            if not wallet_address:
                return Response(
                    {'error': 'No wallet found for user'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                # 1. Lock tokens on blockchain
                blockchain = BlockchainService()
                tx_hash = blockchain.lock_tokens(wallet_address, amount)
                
                # 2. Deduct balance in database
                request.user.profile.deduct_balance(amount)
                
                # 3. Create investment record
                investment = Investment.objects.create(
                    user=request.user,
                    reactor=reactor,
                    amount_invested=amount
                )
                
                # 4. Update reactor funding
                reactor.current_funding += amount
                reactor.save()
                
                response_serializer = InvestmentSerializer(investment)
                return Response({
                    'investment': response_serializer.data,
                    'message': f'Successfully invested {amount:,.2f} $NUC in {reactor.name}',
                    'remaining_balance': float(request.user.profile.balance),
                    'amount_invested': float(amount),
                    'tx_hash': tx_hash,
                    'tx_url': f"https://sepolia.basescan.org/tx/{tx_hash}",
                }, status=status.HTTP_201_CREATED)
            
            except BlockchainError as e:
                return Response(
                    {'error': f'Blockchain error: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def portfolio_summary(self, request):
        """
        Get complete portfolio summary with projections for all time periods (1, 2, 5, 10 years)
            and blockchain balances.
        GET /api/investments/portfolio_summary/
        """
        investments = self.get_queryset()
        wallet_address = request.user.profile.wallet_address
        
        # Get blockchain balances
        wallet_data = None
        if wallet_address:
            try:
                blockchain = BlockchainService()
                wallet_data = {
                    'address': wallet_address,
                    'total': str(blockchain.get_balance(wallet_address)),
                    'locked': str(blockchain.get_locked_balance(wallet_address)),
                    'available': str(blockchain.get_available_balance(wallet_address)),
                    'basescan_url': f"https://sepolia.basescan.org/address/{wallet_address}",
                }
            except BlockchainError:
                # Fallback to database if blockchain unavailable
                wallet_data = {
                    'address': wallet_address,
                    'total': str(request.user.profile.balance),
                    'locked': None,
                    'available': None,
                    'basescan_url': f"https://sepolia.basescan.org/address/{wallet_address}",
                }
        
        if not investments.exists():
            return Response({
                'total_invested': 0,
                'investment_count': 0,
                'reactors_invested_in': [],
                'projections': [],
                'wallet': wallet_data
            })
        
        total_invested = investments.aggregate(
            total=Sum('amount_invested')
        )['total'] or Decimal('0')
        
        reactors_invested_in = list(
            investments.values_list('reactor__name', flat=True).distinct()
        )
        
        time_periods = [1, 2, 5, 10]
        projections = []
        
        for years in time_periods:
            total_roi = Decimal('0')
            total_carbon_offset = Decimal('0')
            
            for investment in investments:
                total_roi += Decimal(str(investment.reactor.calculate_roi_projection(investment.amount_invested, years)))
                total_carbon_offset += Decimal(str(investment.reactor.calculate_carbon_offset_projection(investment.amount_invested, years)))
            
            total_return = total_invested + total_roi
            roi_percentage = (total_roi / total_invested * 100) if total_invested > 0 else Decimal('0')
            
            projections.append({
                'time_period_years': years,
                'total_roi': total_roi,
                'total_carbon_offset': total_carbon_offset,
                'total_return': total_return,
                'roi_percentage': roi_percentage
            })
        
        summary_data = {
            'total_invested': total_invested,
            'investment_count': investments.count(),
            'reactors_invested_in': reactors_invested_in,
            'projections': projections
        }
        
        serializer = PortfolioSummarySerializer(summary_data)
        return Response({
            **serializer.data,
            'wallet': wallet_data
        })