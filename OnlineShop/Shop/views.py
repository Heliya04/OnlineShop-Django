from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view, permission_classes ,APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import generics,status,permissions,viewsets
from rest_framework.views import Response
from rest_framework.generics import ListAPIView
from .serializers import *
from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from rest_framework.pagination import PageNumberPagination
from django.views.generic.list import ListView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import os
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


#html views / render
def compair(request):
    return render(request=request, template_name="compair.html")
def components(request):
    return render(request=request, template_name="components.html")
def contact(request):
    return render(request=request, template_name="contact.html")
def faq(request):
    return render(request=request, template_name="faq.html")
def index(request):
    return render(request=request, template_name="index.html")
def legal_notice(request):
    return render(request=request, template_name="legal_notice.html")
def normal(request):
    return render(request=request, template_name="normal.html")
def product_summary(request):
    return render(request=request, template_name="product_summary.html")
def product_details(request):
    return render(request=request, template_name="product_details.html")
def products(request):
    return render(request=request, template_name="products.html")
def special_offer(request):
    return render(request=request, template_name="special_offer.html")
def tac(request):
    return render(request=request, template_name="tac.html")

#................................................................................................
#  CRUD PRODUCT 

# @api_view(['POST']) 
# @permission_classes([IsAdminUser])
# def create_pro(request, category_pk):
#     category = get_object_or_404(Category, pk=category_pk)
#     product=CreateProductSerializer(data=request.data)
#     if product.is_valid():
#         product.save()
#         return Response(product.data, status=status.HTTP_201_CREATED)
#     return Response(product.errors, status=status.HTTP_400_BAD_REQUEST)

#CLASS_BASE CREATE PRODUCT:
class CreatingProducts(APIView):
    permission_classes=[IsAdminUser]    
    def get(self, request):
        p_product = Product.objects.all()
        serializer = ProductSerializer(p_product, many=True)
        return Response(data=serializer.data , status=status.HTTP_200_OK)
    def post(self , request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST) 

@api_view(['get'])
@permission_classes([IsAdminUser])
def reading_pro(request):
    product=Product.objects.all()
    serializer=ProductSerializer(product, many=True)
    return Response(serializer.data)

#CLASS-BASE READING PRODUCT:
class ProductListView(generics.ListAPIView):
    queryset=Product.objects.all()
    serializer_class= ProductSerializer

@api_view(['PUT']) #is an http method that is used to create or update a resource on a server
@permission_classes([IsAdminUser])
def update_pro(request,pk):
    try:
        product=Product.objects.get(pk=pk) #primary key
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer=ProductSerializer(instance=product, data=request.data) #instance is typically passed to thr serializer when it's created
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#CLASS-BASE UPDATING PRODUCT:
class ProductUpdateView(generics.RetrieveUpdateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field="pk"
    
@api_view(['DELETE']) # is a method on the retrieved product instance to remove it from the database. 
@permission_classes([IsAdminUser])
def delete_pro(requset, pk):
    try:
        product=Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT) #Return a 204 No Content response to indicate successful deletion.

#CLASS-BASE DELETING PRODUCT:
class ProductDeleteView(generics.DestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset=Product.objects.all()
#................................................................................................
#CRUD CATEGORY

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_category(request):
    serializer=CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#CLASS-BASE CREATING CATEGORY:
class CategoryCreateView(generics.CreateAPIView): #method=POST
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def read_category(request):
    categories=Category.objects.all()
    serializer=CategorySerializer(categories, many=True)
    return Response(serializer.data)

#CLASS-BASE READING CATEGORY:
class CategoryListView(generics.ListAPIView):
    permission_classes=[IsAdminUser]
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_category(request, pk):
    try:
        category= Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer=CategorySerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#CLASS-BASE UPDATING CATEGORY:
class CategoryUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes=[IsAdminUser]
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_category(request, pk):
    try:
        category=Category.objects.get(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

#CLASS-BASE DELETING CATEGORY:
class CategoryDeleteView(generics.DestroyAPIView):
    queryset=Category.objects.all()
    permission_classes=[IsAdminUser]
#................................................................................................
# CRUD ORDER


@api_view(['GET'])
@permission_classes([IsAdminUser])
def reading_order(request):
    orders=Order.objects.filter(user=request.user)
    serializer=OrderSerializer(orders, many=True)
    return Response(serializer.data)

#CLASS-BASE READING ORDER:
class OrderListView(generics.ListAPIView):
    permission_classes=[IsAdminUser]
    queryset=Order.objects.all()
    serializer_class=OrderSerializer

# class OrderUpdateView(generics.RetrieveUpdateAPIView):
#     permission_classes=[IsAdminUser]
#     queryset=Order.objects.all()
#     serializer_class=OrderSerializer
#     def perform_update(self, serializer):
#         serializer.save()
            
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_order(request, pk):
    try:
        order=Order.objects.get(pk=pk, user=request.user)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
#CLASS-BASE DELETING ORDER:
class OrderDeleteView(generics.DestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    def get_object(self):
        return Order.objects.get(pk=self.kwargs['pk'], user=self.request.user)

#................................................................................................
# CRUD ORDERITEM

@api_view(['GET'])
@permission_classes([IsAdminUser])
def reading_orderitem(request):
    orders=OrderItem.objects.filter(user=request.user)
    serializer=OrderItemSerializer(orders, many=True)
    return Response(serializer.data)

#CLASS-BASE READING ORDER:
class OrderItemListView(generics.ListAPIView):
    permission_classes=[IsAdminUser]
    queryset=OrderItem.objects.all()
    serializer_class=OrderItemSerializer
    
# CLASS-BASE UPDATING ORDER:
class OrderItemUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes=[IsAdminUser]
    queryset=OrderItem.objects.all()
    serializer_class=OrderItemSerializer
    def perform_update(self, serializer):
        serializer.save()

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_orderitem(request, pk):
    try:
        order=OrderItem.objects.get(pk=pk, user=request.user)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
#CLASS-BASE DELETING ORDER:
class OrderItemDeleteView(generics.DestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset=OrderItem.objects.all()
    serializer_class=OrderItemSerializer
    def get_object(self):
        return OrderItem.objects.get(pk=self.kwargs['pk'], user=self.request.user)
#................................................................................................
# CRUD USER
class UserList(ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    
def register(request):
    return render(request=request, template_name="register.html")
class RegisterAPIView(generics.GenericAPIView): 
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data 
        serializer = self.serializer_class(data=user)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

def login(request):    
    return render(request=request, template_name="login.html")
class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response=super().post(request, *args, **kwargs) 
        status_code=response.status_code
        if status_code==status.HTTP_200_OK:
            refresh=RefreshToken.for_user(request.user)
            response.data['refresh_token']=str(refresh)
            response.data['access_token']=str(refresh.access_token)
        return response    

@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token is None:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(refresh_token)
        return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    


def forgetpass(request):
    return render(request=request, template_name="forgetpass.html")
class RequestPasswordReset(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User with this email not found"}, status=status.HTTP_404_NOT_FOUND)
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        reset = PasswordReset.objects.create(email=email, token=token)
        return Response({"success": "We have sent you a link to reset your password."}, status=status.HTTP_200_OK)
 
# class PasswordResetConfirmView(APIView):
#     def post(self, request):
#         serializer = ResetPasswordRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             new_password = serializer.validated_data['new_password']
#             # Validate and set the new password
#             try:
#                 validate_password(new_password, user)
#             except Exception as e:
#                 return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#             # Set the new password and save the user
#             user.set_password(new_password)
#             user.save()
#             return Response({"detail": "Password has been successfully reset."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#................................................................................................
#cart
class ProductsCart(APIView):
    def post(self, request):
        p_id=request.data["p_id"] #product id
        cart= request.COOKIES.get("cart") # checks if the cart cookies exist
        if cart == None:
            cart=[p_id] # create a new cart
        else:
            cart.append(p_id)
        p=Response(status=status.HTTP_200_OK)
        p.cookies["cart"]=cart 
        return p
    def get(self, request):
        p_product=Product.objects.all()
        result=CreateProductSerializer(p_product, many=True) #serializer
        p=Response(data=result.data, status=status.HTTP_200_OK)
        #p.cookies['salam']=2
        return p


#Pagination   
def index2(request):
    product= Product.objects.all()
    p= Paginator(product , 1)
    n_page=request.GET.get('page')
    try:
        page_obj=p.page(1)
    except PageNotAnInteger: #if page is not an integer then assign the first page
        page_obj=p.page(1)
    except EmptyPage: #if page is empty then return last page
        page_obj=p.page(p.num_pages)
    return render (request=request, context = {'page_obj':page_obj} , template_name="index2.html")
 
class ProductView(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    pagination_class=PageNumberPagination #یک کلاس پیش فرض است که صفحات را بر اساس شماره صفحه تقسیم میکند

class ProductListView(ListView):
    model=Product
    template_name="products.html"
    paginate_by=10
    queryset=Product.objects.all()

@api_view(['GET'])
def get_pro(request):
    product=Product.objects.all()
    paginator=PageNumberPagination() #creates a paginator instance
    page=paginator.nonepaginate_queryset(product, request) #paginates the queryset based on the request parameters
    if page is not None: #if pagination is applied, the paginated queryset is serialized
        serializer=ProductSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    serializer=ProductSerializer(product,many=True)
    return Response(serializer.data)