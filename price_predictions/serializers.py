from rest_framework import serializers
from .models import TomatoMarketData, TomatoPricePrediction

class TomatoMarketDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TomatoMarketData
        fields = ['market', 'date', 'supply_volume', 'wholesale_price', 'retail_price', 'created_at']
        read_only_fields = ['created_at']

    def validate_supply_volume(self, value):
        """Ensure supply volume is positive."""
        if value <= 0:
            raise serializers.ValidationError("Supply volume must be greater than zero.")
        return value

class TomatoPricePredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TomatoPricePrediction
        fields = ['market_data', 'predicted_price', 'prediction_date', 'created_at']
        read_only_fields = ['created_at']

    def validate_predicted_price(self, value):
        """Ensure predicted price is a positive number."""
        if value <= 0:
            raise serializers.ValidationError("Predicted price must be greater than zero.")
        return value
