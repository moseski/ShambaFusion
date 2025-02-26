# from rest_framework import serializers
# from Farm_Insights.models import *

# class FarmInsightsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FarmInsights
#         fields = ['crop_type', 'crop_stage', 'insights']
#         read_only_fields = ['insights']

#     def validate(self, data):
#         """
#         Validate the incoming data for crop_type and crop_stage.
#         """
#         if 'crop_stage' in data and 'crop_type' in data:
#             if data['crop_stage'] == 'seedling' and data['crop_type'] == 'french beans':
#                 raise serializers.ValidationError("French beans should not be at the seedling stage.")
#         return data
#         fields = ['crop_type', 'crop_stage', 'insights', 'created_at']
#         read_only_fields = ['crop_type', 'crop_stage', 'insights', 'created_at']
from rest_framework import serializers
from Farm_Insights.models import FarmInsights

class FarmInsightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmInsights
        fields = ['crop_type', 'crop_stage', 'insights', 'created_at']
        read_only_fields = ['insights', 'created_at']

    def validate(self, data):
        """
        Validate the incoming data for crop_type and crop_stage.
        """
        if 'crop_stage' in data and 'crop_type' in data:
            if data['crop_stage'] == 'seedling' and data['crop_type'] == 'french beans':
                raise serializers.ValidationError("French beans should not be at the seedling stage.")
        return data

    def create(self, validated_data):
        """
        Override the create method to handle generating insights.
        """
        # Create a new FarmInsights instance
        instance = FarmInsights.objects.create(**validated_data)
        
        # Automatically generate insights after creation
        instance.insights = instance.generate_ai_insights()
        instance.save()
        
        return instance
