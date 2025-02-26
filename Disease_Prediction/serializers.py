from rest_framework import serializers
from Disease_Prediction.models import *

class DiseaseSerializer(serializers.ModelSerializer):
    # These fields can be read-only since they are automatically populated after the image is processed
    additional_info = serializers.ReadOnlyField()
    symptoms = serializers.ReadOnlyField()
    treatment = serializers.ReadOnlyField()
    class Meta:
        model = Disease
        fields = ['crop_type', 'image', 'symptoms', 'treatment', 'additional_info']