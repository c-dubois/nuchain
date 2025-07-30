from rest_framework import serializers
from .models import Reactor

class ReactorSerializer(serializers.ModelSerializer):
    
    funding_percentage = serializers.ReadOnlyField()
    available_funding = serializers.ReadOnlyField()
    is_fully_funded = serializers.ReadOnlyField()

    class Meta:
        model = Reactor
        fields = [
            'id',
            'name',
            'slug',
            'type',
            'description',
            'location',
            'annual_roi_rate',
            'carbon_offset_tonnes_co2_per_nuc_per_year',
            'total_funding_needed',
            'current_funding',
            'funding_percentage',
            'available_funding',
            'is_fully_funded',
            'image_url',
            'is_active',
            'created_at'
        ]