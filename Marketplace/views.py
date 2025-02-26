from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import OrderTracking, CheckOut, Order
from .serializers import OrderTrackingSerializer, CheckOutSerializer,  OrderSerializer


# OrderTracking APIs

@api_view(['GET'])
def get_orders(request):
    orders = OrderTracking.objects.all().order_by('-id')
    serializer = OrderTrackingSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_order(request, pk):
    try:
        order = OrderTracking.objects.get(pk=pk)
    except OrderTracking.DoesNotExist:
        return Response({"error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)
    serializer = OrderTrackingSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def post_order(request):
    data = request.data
    serializer = OrderTrackingSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_order(request, pk):
    try:
        order = OrderTracking.objects.get(pk=pk)
    except OrderTracking.DoesNotExist:
        return Response({"error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)
    serializer = OrderTrackingSerializer(order, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_order(request, pk):
    try:
        order = OrderTracking.objects.get(pk=pk)
    except OrderTracking.DoesNotExist:
        return Response({'message': 'The order you are trying to delete was not found'})
    order.delete()
    return Response({'message': 'Order deleted'}, status=status.HTTP_204_NO_CONTENT)


# CheckOut APIs

@api_view(['GET'])
def get_checkouts(request):
    checkouts = CheckOut.objects.all().order_by('-created_at')
    serializer = CheckOutSerializer(checkouts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_checkout(request, pk):
    try:
        checkout = CheckOut.objects.get(pk=pk)
    except CheckOut.DoesNotExist:
        return Response({"error": "Checkout does not exist"}, status=status.HTTP_404_NOT_FOUND)
    serializer = CheckOutSerializer(checkout)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def post_checkout(request):
    data = request.data
    serializer = CheckOutSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_checkout(request, pk):
    try:
        checkout = CheckOut.objects.get(pk=pk)
    except CheckOut.DoesNotExist:
        return Response({"error": "Checkout does not exist"}, status=status.HTTP_404_NOT_FOUND)
    serializer = CheckOutSerializer(checkout, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_checkout(request, pk):
    try:
        checkout = CheckOut.objects.get(pk=pk)
    except CheckOut.DoesNotExist:
        return Response({'message': 'The checkout you are trying to delete was not found'})
    checkout.delete()
    return Response({'message': 'Checkout deleted'}, status=status.HTTP_204_NO_CONTENT)


# Order APIs

@api_view(['GET'])
def get_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def post_order(request):
    data = request.data
    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)
    serializer = OrderSerializer(order, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({'message': 'The order you are trying to delete was not found'}, status=status.HTTP_404_NOT_FOUND)
    order.delete()
    return Response({'message': 'Order deleted'}, status=status.HTTP_204_NO_CONTENT)