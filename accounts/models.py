from django.db import models

# Create your models here.
# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150)
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)


from django.db import models
from django.conf import settings

# class Listing(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     location = models.CharField(max_length=100)
#     seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

from django.db import models
from django.conf import settings

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# class Category(models.Model):
#     name = models.CharField(max_length=100)


class Listing(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    # property_type = models.CharField(max_length=50)
    # category_name = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    square_feet = models.IntegerField()
    year_built = models.IntegerField()
    photo_main = models.ImageField(upload_to='property_photos')
    photo_1 = models.ImageField(blank=True, upload_to='property_photos')
    photo_2 = models.ImageField(blank=True, upload_to='property_photos')
    photo_3 = models.ImageField(blank=True, upload_to='property_photos')
    photo_4 = models.ImageField(blank=True, upload_to='property_photos')
    photo_5 = models.ImageField(blank=True, upload_to='property_photos')
    photo_6 = models.ImageField(blank=True, upload_to='property_photos')
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=15, blank=False, null=True)
    email = models.EmailField(blank=False, null=True)


    def __str__(self):
        return self.title
    


class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20,blank=False, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Inquiry from {self.name}'

# from django.db import models
# from django.contrib.auth.models import User

# class Property(models.Model):
#     seller = models.ForeignKey(User, on_delete=models.CASCADE)
#     address = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     # Add more fields as needed

#     def __str__(self):
#         return self.address


