from django.db import models
from shamba.models import User

# Create your models here.
class Product(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
   
class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products')
    description = models.TextField()    
    
    def __str__(self):
        return self.name