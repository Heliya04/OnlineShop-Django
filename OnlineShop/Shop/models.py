from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here

class Category(models.Model):
    name=models.CharField(max_length=255)
    
class Product(models.Model):
    category=models.ForeignKey(Category , on_delete=models.SET_NULL , null=True)
    title=models.CharField(max_length=255)
    count=models.IntegerField(default=0)
    price=models.IntegerField()
    desc=models.TextField(default="")
    modified=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    
class User(AbstractUser):
    phone_number=models.CharField(max_length=11 , null=True)
    address=models.TextField(null=True)   
    role=models.IntegerField(default=0)

class Order(models.Model): 
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product= models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)
    order_date=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.PositiveIntegerField(default=0)

    
class OrderItem(models.Model): 
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0) 
    #PositiveIntegerField =to save positive integer values
    total_amount=models.DecimalField(max_digits=10, decimal_places=2 ) 
    # DecimalField=to save decimal numbers/Cuurency/measurements/percentages
    #decimal_places = the number of decimal places allowed    
    
class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

#class BlacklistedToken(models.Model):
    #token=models.CharField(max_length=255, unique=True)
