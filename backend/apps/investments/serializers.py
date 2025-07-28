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