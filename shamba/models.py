from django.db import models
import requests
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from django.utils import timezone
import numpy as np
import os
# Create your models here.
class User(AbstractUser):
    SELLER = 'seller'
    BUYER = 'buyer'
    VENDOR = 'vendor'
    
    USER_ROLE_CHOICES = [
        (SELLER, 'seller'),
        (BUYER, 'Buyer'),
        (VENDOR, 'Vendor'),
    ]
    
    user_role = models.CharField(
        max_length=10,
        choices=USER_ROLE_CHOICES,
        default=SELLER,
    )

    def is_seller(self):
        return self.user_role == self.SELLER

    def is_buyer(self):
        return self.user_role == self.BUYER
    
    def is_vendor(self):
        return self.user_role == self.VENDOR
   
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name
    