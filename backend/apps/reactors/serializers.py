from rest_framework import serializers
from .models import Reactor

class ReactorSerializer(serializers.ModelSerializer):
    
    investment_percentage = serializers.ReadOnlyField()
    available_capacity = serializers.ReadOnlyField()
    is_fully_funded = serializers.ReadOnlyField()

    class Meta:
        model = Reactor
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'location',
            'price_per_token',
            'annual_roi_rate',
            'carbon_offset_per_token_per_year',
            'total_token_capacity',
            'current_investments',
            'investment_percentage',
            'available_capacity',
            'is_fully_funded',
            'image_url',
            'is_active',
            'created_at'
        ]

# class ReactorProjectionSerializer(serializers.Serializer):
#     """Serializer for ROI and carbon offset projections"""
#     token_amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)
#     time_period_years = serializers.IntegerField(min_value=1, max_value=10)

#     def validate_time_period_years(self, value):
#         """Ensure time period is one of the allowed values"""
#         allowed_time_periods = [1, 2, 5, 10]
#         if value not in allowed_time_periods:
#             raise serializers.ValidationError(f"Time period must be one of: {allowed_time_periods}")
#         return value