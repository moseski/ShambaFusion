from django.db import models
from shamba.models import User
from Farm_Products.models import Product

# Create your models here.


class OrderTracking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    # order_id = models.CharField(max_length=100, unique=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    tracking_number = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f'Order for {self.buyer} - {self.product_name} - {self.quantity} - {self.tracking_number}'
    
    
class CheckOut(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment for {self.buyer} - {self.price}'
    

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name    