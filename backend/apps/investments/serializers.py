from rest_framework import serializers
from .models import Investment
from apps.reactors.serializers import ReactorSerializer

class InvestmentSerializer(serializers.ModelSerializer):
    reactor = ReactorSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Investment
        fields = [
            'id',
            'user',
            'reactor',
            'amount_invested',
            'created_at'
        ]

class CreateInvestmentSerializer(serializers.ModelSerializer):
    reactor_id = serializers.IntegerField()

    class Meta:
        model = Investment
        fields = ['reactor_id', 'amount_invested']

    def validate_investment(self, data):
        """Validate the investment"""
        from apps.reactors.models import Reactor

        try:
            reactor = Reactor.objects.get(id=data['reactor_id'], is_active=True)
        except Reactor.DoesNotExist:
            raise serializers.ValidationError("Reactor not found or inactive")
        
        amount = data['amount_invested']

        if not reactor.can_invest(amount):
            raise serializers.ValidationError({
                'amount_invested': f"Cannot invest {amount:,.2f} $NUC. Available capacity: {reactor.available_capacity:,.2f} $NUC"
            })
        
        user = self.context['request'].user
        total_cost = amount * reactor.price_per_token

        if not user.profile.can_afford(total_cost):
            raise serializers.ValidationError({
                'amount_invested': f"Insufficient balance. Cost: {total_cost:,.2f} $NUC; Your balance: {user.profile.balance:,.2f} $NUC"
            })
        
        data['reactor'] = reactor
        return data
    
class PortfolioProjectionSerializer(serializers.Serializer):
    """Serializer for portfolio projections across time periods: 1, 2, 5, 10 years"""
    time_period_years = serializers.IntegerField()
    total_roi = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_carbon_offset = serializers.DecimalField(max_digits=12, decimal_places=4)
    total_return = serializers.DecimalField(max_digits=15, decimal_places=2)
    roi_percentage = serializers.DecimalField(max_digits=8, decimal_places=2)

class PortfolioSummarySerializer(serializers.Serializer):
    """Serializer for user's complete portfolio summary"""
    total_invested = serializers.DecimalField(max_digits=15, decimal_places=2)
    investment_count = serializers.IntegerField()
    reactors_invested_in = serializers.ListField(child=serializers.CharField())
    projections = PortfolioProjectionSerializer(many=True)