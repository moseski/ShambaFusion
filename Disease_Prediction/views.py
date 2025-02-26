from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.http import JsonResponse
from Disease_Prediction.models import Disease
from rest_framework import status

@api_view(['POST'])
@parser_classes([MultiPartParser])
def analyze_disease(request):
    # Retrieve crop_type from the request data
    crop_type = request.data.get('crop_type')
    
    # Ensure 'crop_type' is provided
    if not crop_type:
        return JsonResponse({'error': 'crop_type is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if an image file is provided in the request
    img_file = request.FILES.get('image')
    if not img_file:
        return JsonResponse({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Create a new Disease instance with crop_type and image
        disease = Disease(crop_type=crop_type, image=img_file)
        disease.save()  # Save to trigger any overridden save methods in the Disease model

        # Prepare the response data
        response_data = {
            'crop_type': disease.crop_type,
            'symptoms': disease.symptoms,
            'treatment': disease.treatment,
            'additional_info': disease.additional_info
        }

        # Return the JSON response
        return JsonResponse(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        # Log the exception for debugging
        print(f"Error in analyze_disease view: {e}")
        
        # Return an error response with a message
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# # # from django.shortcuts import render
# # from Disease_Prediction.serializers import *
# # from rest_framework import viewsets, generics, status
# # from rest_framework.decorators import action
# # from rest_framework.response import Response
# # from rest_framework.decorators import api_view
# # from .models import Disease


# # # class DiseaseViewSet(viewsets.ModelViewSet):
# #     queryset = Disease.objects.all()
# #     serializer_class = DiseaseSerializer

# #     def create(self, request, *args, **kwargs):
# #         serializer = self.get_serializer(data=request.data)
# #         serializer.is_valid(raise_exception=True)
# #         disease = serializer.save()
# #         return Response(DiseaseSerializer(disease).data, status=status.HTTP_201_CREATED)

# #     def update(self, request, *args, **kwargs):
# #         instance = self.get_object()
# #         serializer = self.get_serializer(instance, data=request.data)
# #         serializer.is_valid(raise_exception=True)
# #         disease = serializer.save()
# #         return Response(DiseaseSerializer(disease).data, status=status.HTTP_200_OK)

# #     def partial_update(self, request, *args, **kwargs):
# #         instance = self.get_object()
# #         serializer = self.get_serializer(instance, data=request.data, partial=True)
# #         serializer.is_valid(raise_exception=True)
# #         disease = serializer.save()
# #         return Response(DiseaseSerializer(disease).data, status=status.HTTP_200_OK)

# #     def destroy(self, request, *args, **kwargs):
# #         instance = self.get_object()
# #         instance.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)

# #     @action(detail=True, methods=['post'])
# #     def predict(self, request, pk=None):
# #         return Response({"prediction": "predicted disease name"}, status=status.HTTP_200_OK)

# #     @action(detail=True, methods=['get'])
# #     def translate(self, request, pk=None):
# #         return Response({"translated_name": "Translated Disease Name"}, status=status.HTTP_200_OK)

# #     @action(detail=True, methods=['post'])
# #     def fetch_external_data(self, request, pk=None):
# #         return Response({"external_data": "Data fetched from API"}, status=status.HTTP_200_OK)

# # @api_view(['POST'])
# # def post_disease(request):
# #     """Endpoint to create a new disease prediction based on uploaded image and generate related info."""
# #     serializer = DiseaseSerializer(data=request.data)
# #     if serializer.is_valid():
# #         disease = serializer.save()
# #         return Response(DiseaseSerializer(disease).data, status=status.HTTP_201_CREATED)
# #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# import os
# import openai
# import numpy as np
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from keras.models import load_model
# from keras.preprocessing import image
# from rest_framework.parsers import MultiPartParser
# from rest_framework.decorators import api_view, parser_classes

# # Load the trained Keras model once at startup
# model_path = os.path.join('/home/dominic/Shamba/disease_detection_model.keras')
# model = load_model(model_path)

# # Define class labels for disease prediction
# class_labels = [
#     'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Tomato_Bacterial_spot',
#     'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold',
#     'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two_spotted_spider_mite',
#     'Tomato__Target_Spot', 'Tomato__Tomato_mosaic_virus', 'Tomato__Tomato_YellowLeaf__Curl_Virus',
#     'Tomato_healthy'
# ]

# # OpenAI API setup
# openai.api_key = os.getenv('AZURE_OPENAI_API_KEY')

# def get_disease_info(disease_name):
#     prompt = (
#         f"Give detailed information about the disease '{disease_name}', including symptoms, causes, "
#         "possible treatments, and recommended actions. Translate this information into both English and Swahili."
#     )

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=500,
#             temperature=0.7
#         )
#         return response.choices[0].message['content'].strip()
#     except openai.error.OpenAIError as e:
#         return f"Error: {e}"

# @csrf_exempt
# @api_view(['POST'])
# @parser_classes([MultiPartParser])
# def analyze_disease(request):
#     if 'image' not in request.FILES:
#         return JsonResponse({'error': 'No image provided'}, status=400)

#     # Load the image from the request
#     img_file = request.FILES['image']
#     img = image.load_img(img_file, target_size=(224, 224))
#     img_array = image.img_to_array(img)
#     img_array = np.expand_dims(img_array, axis=0)
#     img_array /= 255.0

#     # Predict disease
#     predictions = model.predict(img_array)
#     predicted_index = np.argmax(predictions)
#     disease_name = class_labels[predicted_index]
#     confidence_level = float(np.max(predictions)) * 100

#     # Fetch disease details using OpenAI API
#     disease_info = get_disease_info(disease_name)

#     # Parse out structured data (e.g., symptoms, causes, actions)
#     return JsonResponse({
#         'detectedDisease': disease_name,
#         'confidenceLevel': f"{confidence_level:.2f}%",
#         'diseaseInfo': disease_info
#     })



# from django.http import JsonResponse
# from rest_framework.decorators import api_view, parser_classes
# from rest_framework.parsers import MultiPartParser
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Disease
# from .serializers import DiseaseSerializer


# @api_view(['POST'])
# @parser_classes([MultiPartParser])
# def analyze_disease(request):
#     if 'image' not in request.FILES:
#         return JsonResponse({'error': 'No image provided'}, status=400)
    
#     # Save the disease instance and let it handle the prediction
#     disease = Disease(
#         crop_type=request.data.get('crop_type'),
#         image=request.FILES['image']
#     )
    
#     disease = Disease(crop_type=crop_type, image=img_file)
#     disease.save()

#     # Serialize the saved instance
#     serializer = DiseaseSerializer(disease)
#     return Response(serializer.data, status=status.HTTP_201_CREATED)



# from rest_framework.decorators import api_view, parser_classes
# from rest_framework.parsers import MultiPartParser
# from rest_framework.response import Response
# from django.http import JsonResponse
# from Disease_Prediction.models import Disease
# from rest_framework import status

# @api_view(['POST'])
# @parser_classes([MultiPartParser])
# def analyze_disease(request):
#     # print(request.data)  # Check the actual request data
#     # print(request.FILES)  # Check the uploaded files

#     # crop_type = request.data.get('crop_type')
#     # img_file = request.FILES.get('image')

#     # Retrieve crop_type from request data
#     crop_type = request.data.get('crop_type')
    
#     # Ensure 'crop_type' is provided
#     if not crop_type:
#         return JsonResponse({'error': 'crop_type is required'}, status=400)

#     # Check if image file is provided in the request
#     img_file = request.FILES.get('image')
#     if not img_file:
#         return JsonResponse({'error': 'No image file provided'}, status=400)
    
#     try:
#         # Create a new Disease instance with crop_type and image
#         disease = Disease(crop_type=crop_type, image=img_file)
#         disease.save()  # This will trigger the overridden save method
        
#         # additional_info = disease.fetch_additional_info()
#         return JsonResponse({
#             'crop_type': disease.crop_type,
#             'symptoms': disease.symptoms,
#             'treatment': disease.treatment,
#             'additional_info': disease.additional_info
#         }, status=status.HTTP_201_CREATED)
    
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
