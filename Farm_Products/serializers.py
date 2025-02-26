from rest_framework import serializers
from .models import Product, Category
from django.contrib.auth import authenticate, login

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'image': {'required': False}
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'    
        extra_kwargs = {
            'image': {'required': False}
        }    
        
      