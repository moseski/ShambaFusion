from django.db import models

class TomatoMarketData(models.Model):
    MARKET_LOCATIONS = [
        ('nairobi', 'Nairobi'),
        ('mombasa', 'Mombasa'),
        ('kisumu', 'Kisumu'),
        ('eldoret', 'Eldoret'),
    ]

    market = models.CharField(max_length=50, choices=MARKET_LOCATIONS)
    date = models.DateField()
    supply_volume = models.IntegerField(help_text="Supply volume in kilograms")
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Wholesale price per kg")
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Retail price per kg")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tomato Prices in {self.market} on {self.date}"

class TomatoPricePrediction(models.Model):
    market_data = models.ForeignKey(TomatoMarketData, on_delete=models.CASCADE, related_name="predictions")
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Predicted price per kg")
    prediction_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Predicted Price on {self.prediction_date}: {self.predicted_price}"
