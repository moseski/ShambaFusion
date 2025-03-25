from django.db import models

class PricePrediction(models.Model):
    """Model to store crop price predictions"""
    created_at = models.DateTimeField(auto_now_add=True)
    crop_type = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    supply_volume = models.FloatField()
    market = models.CharField(max_length=100)
    wholesale_price = models.FloatField()
    retail_price = models.FloatField()
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Price Prediction'
        verbose_name_plural = 'Price Predictions'
    
    def __str__(self):
        return f"{self.crop_type} in {self.county} at {self.market}"