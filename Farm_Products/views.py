from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from django.core.mail import send_mail
from .models import *
from .serializers import *
# Create your views here.
from .serializers import ProductSerializer

#Product Apis   
@api_view(['GET'])
def get_products(request):
    products = Product.objects.all().order_by('created_at')
    serializer = ProductSerializer(products,  many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])    
def get_product( request, pk):
        try:   
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
             return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
@api_view(['POST'])
def post_product(request):
    # Print incoming data and files for debugging
    print("Request data:", request.data)
    print("Request files:", request.FILES)

    # Copy request data to make it mutable, add farmer ID
    data = request.data.copy()
    # data['farmer'] = request.user.id

    # Initialize the serializer
    serializer = ProductSerializer(data=data)

    # Check if the serializer is valid and save if it is
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Print serializer errors if validation fails
    print("Serializer errors:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_product(request, pk):
    try:
        # Fetch the product by primary key
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user is authorized to update the product
    if product.farmer != request.user:
        return Response({"error": "Not authorized to update the product"}, status=status.HTTP_403_FORBIDDEN)

    # Copy request data to make it mutable and update if needed
    data = request.data.copy()
    # data['farmer'] = request.user.id  # Uncomment if farmer ID is required

    # Initialize the serializer with the product instance and updated data
    serializer = ProductSerializer(product, data=data, partial=True)  # partial=True allows for partial updates

    # Validate and save the updated product
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Print serializer errors if validation fails
    print("Serializer errors:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def delete_product( request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:  
            return Response({'message': 'the product you trying to delete not found'})  
        
        if product.farmer != request.user:
            return Response({"error": "You are not authorized to delete this product"}, status=status.HTTP_403_FORBIDDEN)
        
        product.delete()
        return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)



#Category Apis   
@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all().order_by('created_at')
    serializer = CategorySerializer(categories,  many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])    
def get_category( request, pk):
        try:   
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
             return Response({"error": "Category does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
@api_view(['POST'])
def post_category(request):
        data = request.data
        serializer = CategorySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
           
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PUT'])
def update_category( request, pk):
        try:   
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
             return Response({"error": "Category does not exist"}, status=status.HTTP_404_NOT_FOUND)    
        
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 



@api_view(['DELETE'])
def delete_category( request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:  
            return Response({'message': 'the category you trying to delete not found'})  
        
        category.delete()
        return Response({'message': 'Category deleted'}, status=status.HTTP_204_NO_CONTENT)

