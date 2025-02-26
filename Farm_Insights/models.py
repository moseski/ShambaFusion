from django.conf import settings
import openai
from django.db import models
# from django.contrib.auth.models import User

class FarmInsights(models.Model):
    CROP_STAGES = [
        ('planting', 'Planting'),
        ('seedling', 'Seedling'),
        ('vegetative', 'Vegetative'),
        ('flowering', 'Flowering'),
        ('fruiting', 'Fruiting'),
        ('harvesting', 'Harvesting')
    ]

    CROP_TYPES = [
        ('tomatoes', 'Tomatoes'),
        # ('french beans', 'French Beans')
    ]

    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    crop_type = models.CharField(max_length=30, choices=CROP_TYPES)
    crop_stage = models.CharField(max_length=30, choices=CROP_STAGES)
    insights = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Insights for {self.crop_type}'

    def generate_ai_insights(self):
        """Generate insights using Azure OpenAI API."""
        openai.api_key = settings.AZURE_OPENAI_API_KEY
        openai.api_base = settings.AZURE_OPENAI_API_ENDPOINT

        prompt = f"Provide smart farming insights for {self.crop_type} during the {self.crop_stage} stage."
        try:
            response = openai.Completion.create(
                engine="gpt-4",
                prompt=prompt,
                max_tokens=150
            )
            ai_insights = response.choices[0].text.strip()
        except Exception as e:
            ai_insights = f"Failed to retrieve AI insights: {e}"

        return ai_insights

    def save(self, *args, **kwargs):
        if not self.insights:
            self.insights = self.generate_ai_insights()
        super().save(*args, **kwargs)

# from django.contrib.auth.models import User
# from django.conf import settings

# # Create your models here.
# class FarmInsights(models.Model):
#     CROP_STAGES = [
#         ('planting', 'Planting'),
#         ('seedling', 'Seedling'),
#         ('vegetative', 'Vegetative'),
#         ('flowering', 'Flowering'),
#         ('fruiting', 'Fruiting'),
#         ('harvesting', 'Harvesting')
#     ]

#     CROP_TYPES = [
#         ('tomatoes', 'Tomatoes'),
#         # ('french beans', 'French Beans')
#     ]

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
#     crop_type = models.CharField(max_length=30, choices=CROP_TYPES)
#     crop_stage = models.CharField(max_length=30, choices=CROP_STAGES)  # Added crop stage field
#     insights = models.TextField(blank=True)  # Insights can be blank initially
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'Insights for {self.crop_type} - {self.user.username}'

#     def generate_insights(self):
#         """Generate insights based on the crop type and stage."""
#         if self.crop_type == 'tomatoes':
#             return self.get_tomato_insights()
#         elif self.crop_type == 'french beans':
#             return self.get_french_beans_insights()
#         else:
#             return "No insights available for this crop."

#     def get_tomato_insights(self):
#         """Generate tomato farming insights based on the current stage."""
#         insights = ""
#         if self.crop_stage == 'planting':
#             insights = "Ensure the soil is well-prepared and use certified seeds. Plant at the right depth for better germination."
#         elif self.crop_stage == 'seedling':
#             insights = "Monitor seedlings for diseases and ensure adequate watering. Use organic fertilizers."
#         elif self.crop_stage == 'vegetative':
#             insights = "Prune excess leaves, monitor pest attacks, and ensure proper fertilization during vegetative growth."
#         elif self.crop_stage == 'flowering':
#             insights = "Control pests like aphids and ensure the crop has enough water to boost flowering."
#         elif self.crop_stage == 'fruiting':
#             insights = "Apply fertilizers high in potassium to encourage fruit growth and monitor for common diseases."
#         elif self.crop_stage == 'harvesting':
#             insights = "Harvest tomatoes when they are fully ripe to avoid spoilage. Use proper storage methods to reduce losses."
#         return insights
#     def save(self, *args, **kwargs):
#             # Automatically generate insights when the instance is saved
#             if not self.insights:  # Generate insights only if not already set
#                 self.insights = self.generate_insights()
#             super().save(*args, **kwargs)
            
