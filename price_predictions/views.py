from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TomatoMarketData, TomatoPricePrediction
from .serializers import TomatoMarketDataSerializer, TomatoPricePredictionSerializer

@api_view(['GET', 'POST'])
def market_data_view(request):
    """
    Retrieve all tomato market data or add new market data.
    """
    if request.method == 'GET':
        market_data = TomatoMarketData.objects.all()
        serializer = TomatoMarketDataSerializer(market_data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TomatoMarketDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def price_prediction_view(request):
    """
    Retrieve predicted tomato prices or add a new prediction.
    """
    if request.method == 'GET':
        predictions = TomatoPricePrediction.objects.all()
        serializer = TomatoPricePredictionSerializer(predictions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TomatoPricePredictionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def market_data_detail_view(request, pk):
    """
    Retrieve details of a specific market data entry.
    """
    market_data = get_object_or_404(TomatoMarketData, pk=pk)
    serializer = TomatoMarketDataSerializer(market_data)
    return Response(serializer.data)

@api_view(['GET'])
def price_prediction_detail_view(request, pk):
    """
    Retrieve details of a specific price prediction.
    """
    prediction = get_object_or_404(TomatoPricePrediction, pk=pk)
    serializer = TomatoPricePredictionSerializer(prediction)
    return Response(serializer.data)
