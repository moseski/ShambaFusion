from rest_framework import serializers
from .models import PricePrediction

class PricePredictionSerializer(serializers.ModelSerializer):
    """Serializer for PricePrediction model"""
    class Meta:
        model = PricePrediction
        fields = '__all__'

class PricePredictionRequestSerializer(serializers.Serializer):
    """Serializer for price prediction requests"""
    crop_type = serializers.CharField(max_length=100)
    county = serializers.CharField(max_length=100)
    supply_volume = serializers.FloatField(min_value=0)
    
    def validate_crop_type(self, value):
        """Validate crop type"""
        valid_crops = [
            "tomatoes", "potatoes", "onions", "maize", "beans", 
            "cabbage", "kale", "carrots", "spinach", "green-peas"
        ]
        if value.lower() not in valid_crops:
            raise serializers.ValidationError(f"Invalid crop type. Choose from: {', '.join(valid_crops)}")
        return value
    
    def validate_county(self, value):
        """Validate county"""
        valid_counties = [
            "nairobi", "mombasa", "kisumu", "nakuru", "kiambu", "machakos",
            "uasin-gishu", "kakamega", "nyeri", "kilifi", "bungoma", "trans-nzoia"
        ]
        if value.lower() not in valid_counties:
            raise serializers.ValidationError(f"Invalid county. Choose from: {', '.join(valid_counties)}")
        return value