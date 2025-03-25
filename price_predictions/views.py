from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
import logging

from .models import PricePrediction
from .serializers import PricePredictionSerializer, PricePredictionRequestSerializer
from .price_predictor import PricePredictor

logger = logging.getLogger(__name__)

class PricePredictionViewSet(viewsets.ModelViewSet):
    """ViewSet for price predictions"""
    queryset = PricePrediction.objects.all()
    serializer_class = PricePredictionSerializer
    
    @action(detail=False, methods=['post'])
    def predict(self, request):
        """Generate price predictions"""
        # Validate request data
        serializer = PricePredictionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get validated data
            crop_type = serializer.validated_data['crop_type']
            county = serializer.validated_data['county']
            supply_volume = serializer.validated_data['supply_volume']
            
            logger.info(f"Generating price prediction for {crop_type} in {county} with supply volume {supply_volume}kg")
            
            # Initialize predictor
            predictor = PricePredictor()
            
            # Generate predictions
            predictions = predictor.predict_prices(
                crop_type=crop_type,
                county=county,
                supply_volume=supply_volume
            )
            
            # Save predictions to database
            saved_predictions = []
            for pred in predictions:
                prediction = PricePrediction.objects.create(
                    crop_type=crop_type,
                    county=county,
                    supply_volume=supply_volume,
                    market=pred['market'],
                    wholesale_price=pred['wholesale'],
                    retail_price=pred['retail']
                )
                saved_predictions.append(prediction)
            
            # Return response
            return Response({
                'crop_type': crop_type,
                'county': county,
                'supply_volume': supply_volume,
                'predictions': predictions
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error processing prediction request: {e}")
            return Response(
                {'error': 'Failed to generate predictions', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        




# Add this method to your PricePredictionViewSet class
@action(detail=False, methods=['post'])
def market_analysis(self, request):
    """Generate market analysis data"""
    try:
        # Get parameters from request
        crop_type = request.data.get('crop_type', 'tomatoes')
        time_period = request.data.get('time_period', '6m')
        
        # This is where you would fetch real data from your database
        # For now, we'll return mock data based on the crop type
        
        # Mock data for different crops
        crop_data = {
            "tomatoes": {
                "marketHistory": [
                    {"date": "Jan", "price": 2.5, "prediction": 2.6},
                    {"date": "Feb", "price": 2.7, "prediction": 2.8},
                    {"date": "Mar", "price": 2.9, "prediction": 3.0},
                    {"date": "Apr", "price": 3.1, "prediction": 3.2},
                    {"date": "May", "price": 3.3, "prediction": 3.4},
                    {"date": "Jun", "price": 3.5, "prediction": 3.6},
                ],
                "priceTrend": [
                    {"month": "Jan", "wholesale": 2.2, "retail": 3.5},
                    {"month": "Feb", "wholesale": 2.4, "retail": 3.7},
                    {"month": "Mar", "wholesale": 2.6, "retail": 3.9},
                    {"month": "Apr", "wholesale": 2.8, "retail": 4.1},
                    {"month": "May", "wholesale": 3.0, "retail": 4.3},
                    {"month": "Jun", "wholesale": 3.2, "retail": 4.5},
                ],
                "supplyVolume": [
                    {"month": "Jan", "volume": 1000},
                    {"month": "Feb", "volume": 1200},
                    {"month": "Mar", "volume": 1400},
                    {"month": "Apr", "volume": 1600},
                    {"month": "May", "volume": 1800},
                    {"month": "Jun", "volume": 2000},
                ],
                "regionalPrices": [
                    {"county": "Nairobi", "price": 3.5},
                    {"county": "Mombasa", "price": 3.8},
                    {"county": "Kisumu", "price": 3.2},
                    {"county": "Nakuru", "price": 3.0},
                    {"county": "Kiambu", "price": 3.3},
                ],
                "marketShare": [
                    {"name": "Wakulima Market", "value": 35},
                    {"name": "Gikomba Market", "value": 25},
                    {"name": "Kongowea Market", "value": 20},
                    {"name": "Other Markets", "value": 20},
                ],
                "seasonalTrend": [
                    {"month": "Jan", "price": 3.2, "demand": 70},
                    {"month": "Feb", "price": 3.5, "demand": 75},
                    {"month": "Mar", "price": 3.7, "demand": 80},
                    {"month": "Apr", "price": 3.9, "demand": 85},
                    {"month": "May", "price": 4.1, "demand": 90},
                    {"month": "Jun", "price": 4.3, "demand": 95},
                    {"month": "Jul", "price": 4.5, "demand": 100},
                    {"month": "Aug", "price": 4.3, "demand": 95},
                    {"month": "Sep", "price": 4.0, "demand": 90},
                    {"month": "Oct", "price": 3.8, "demand": 85},
                    {"month": "Nov", "price": 3.5, "demand": 80},
                    {"month": "Dec", "price": 3.3, "demand": 75},
                ],
                "priceVolatility": 15,
                "averagePrice": 3.2,
                "priceChange": 8.5,
                "supplyGrowth": 12.3,
            },
            # Add data for other crops as needed
        }
        
        # Return data for the requested crop, or tomatoes as default
        return Response(crop_data.get(crop_type, crop_data["tomatoes"]))
        
    except Exception as e:
        logger.error(f"Error generating market analysis: {e}")
        return Response(
            {'error': 'Failed to generate market analysis', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

