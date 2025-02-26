from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FarmInsights
from .serializers import FarmInsightsSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def get_insights(request):
    """
    Retrieve insights for a specific user or create new insights.
    """
    if request.method == 'GET':
        insights = FarmInsights.objects.filter(user=request.user)
        serializer = FarmInsightsSerializer(insights, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FarmInsightsSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.validated_data['user'] = request.user
            insights = serializer.save()
            return Response(FarmInsightsSerializer(insights).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
