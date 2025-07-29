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