from rest_framework import serializers
from .models import *
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings
from datetime import datetime


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields='__all__'

class CreateCategorySerializer(serializers.ModelSerializer):
    products=serializers.SerializerMethodField()
    def get_product(self,obj):
        tmp=Product.objects.get(id=obj.product.id)
        return tmp.title
    class Meta:
        model=Category
        fields=["name","products"]

class CreateProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    def get_category(self, obj):
        tmp=Category.objects.get(id=obj.category.id)
        return tmp.name
    class Meta:
        model=Product
        fields=["title","price","category","count"]
        3
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","first_name","last_name","phone"]
    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        return user

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields='__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'
        
        
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, min_length=5)
    username = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum(): # checking the username contains alphanumeric(letter & numbers) charactors
            raise serializers.ValidationError(self.default_error_messages)
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()
    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'], # longlift token? 
            'access': user.tokens()['access'] # is a token for authenticated users
        }
    class Meta:
        model = User
        fields = ['password','username','tokens']
    def validate(self, attrs):
        username = attrs.get('username','')
        password = attrs.get('password','')
        user = auth.authenticate(username=username,password=password) # try to authenticate the user with username and password
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active: # is_active => user account is active (permission) to login
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist() #invalidate the refresh token
        except TokenError:
            self.fail('bad_token') # is a method is called to trigger a validation error
     
            
class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, min_length=5)
    class Meta:
        model=User
        fields=["email"]
    
class ResetPasswordSerializer(serializers.Serializer):
    uid64=serializers.CharField() #url safe base63-encoded version of the id 
    # at least one uppercase letter
    # at least one digit
    # at least one special character
    # at least 8 characters long
    # #new_password = serializers.RegexField( regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
    #     write_only=True, 
    #     error_messages={'invalid': ('Password must be at least 8 characters long with at least one capital letter and symbol')})
    new_password=serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    token=serializers.CharField()
    def validate(self, attrs):
        new_password = attrs['new_password']
        confirm_password = attrs['confirm_password']
        # Check if the passwords match
        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        # Decode JWT token to get user information
        try:
            payload = self.decode_jwt_token(attrs['token'])
            user_id = payload.get('user_id')
            if not user_id:
                raise serializers.ValidationError({"token": "Invalid token."})
            user = get_user_model().objects.get(id=user_id)
            attrs['user'] = user
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError({"token": "Token has expired."})
        except jwt.InvalidTokenError:
            raise serializers.ValidationError({"token": "Invalid token."})
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError({"user": "User not found."})
        return attrs
    def decode_jwt_token(self, token):
        try:
            # Decoding the JWT token (assuming it's signed with a secret key)
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError({"token": "Token has expired."})
        except jwt.InvalidTokenError:
            raise serializers.ValidationError({"token": "Invalid token."})