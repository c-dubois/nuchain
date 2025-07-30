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
        """Create a new investment"""
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            reactor = serializer.validated_data['reactor']
            amount = serializer.validated_data['amount_invested']

            if request.user.profile.deduct_balance(amount):
                investment = Investment.objects.create(
                    user=request.user,
                    reactor=reactor,
                    amount_invested=amount
                )

                reactor.current_funding += amount
                reactor.save()

                response_serializer = InvestmentSerializer(investment)
                return Response({
                    'investment': response_serializer.data,
                    'message': f'Successfully invested {amount:,.2f} $NUC in {reactor.name}',
                    'remaining_balance': float(request.user.profile.balance),
                    'amount_invested': float(amount)
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'error': 'Insufficient balance'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def portfolio_summary(self, request):
        """
        Get complete portfolio summary with projections for all time periods (1, 2, 5, 10 years)
        GET /api/investments/portfolio_summary/
        """
        investments = self.get_queryset()

        if not investments.exists():
            return Response({
                'total_invested': 0,
                'investment_count': 0,
                'reactors_invested_in': [],
                'projections': []
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
                total_roi += Decimal(str(investment.reactor.calculate_roi_projection(years)))
                total_carbon_offset += Decimal(str(investment.reactor.calculate_carbon_offset_projection(years)))

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
        return Response(serializer.data)
