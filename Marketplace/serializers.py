from rest_framework import serializers
from .models import OrderTracking, CheckOut, Order

# OrderTracking Serializer
class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTracking
        fields = ['id', 'buyer', 'product_name', 'quantity', 'price', 'status', 'tracking_number']

# CheckOut Serializer
class CheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckOut
        fields = ['id', 'buyer', 'product_name', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'buyer', 'product', 'quantity', 'price', 'status', 'created_at']
        # read_only_fields = ['created_at']  