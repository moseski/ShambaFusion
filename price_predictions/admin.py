from django.contrib import admin
from .models import PricePrediction

@admin.register(PricePrediction)
class PricePredictionAdmin(admin.ModelAdmin):
    """Admin interface for PricePrediction model"""
    list_display = ('crop_type', 'county', 'market', 'wholesale_price', 'retail_price', 'created_at')
    list_filter = ('crop_type', 'county', 'market', 'created_at')
    search_fields = ('crop_type', 'county', 'market')
    date_hierarchy = 'created_at'