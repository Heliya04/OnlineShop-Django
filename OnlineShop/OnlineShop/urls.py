"""
URL configuration for OnlineShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#from Shop import views
from Shop.views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
) 
 
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
        
    #API URLS
    #path('api/create_product/<int:category_pk>', create_pro),
    path('api/C_product', CreatingProducts.as_view()),
    path('api/read_product', reading_pro),
    path('api/R_product', ProductListView.as_view()),
    path('api/update_pro/<int:pk>', update_pro),
    path('api/U_product/<int:pk>', ProductUpdateView.as_view()),
    path('api/delete_pro/<int:pk>', delete_pro),
    path('api/D_product/<int:pk>', ProductDeleteView.as_view()),
    
    path('api/create_category/<int:pk>', create_category),
    path('api/C_category/<int:pk>', CategoryCreateView.as_view()),
    path('api/read_category', read_category),
    path('api/R_category', CategoryListView.as_view()),
    path('api/update_category/<int:pk>', update_category),
    path('api/U_category/<int:pk>', CategoryUpdateView.as_view()),
    path('api/delete_category/<int:pk>', delete_category),
    path('api/D_category/<int:pk>', CategoryDeleteView.as_view()),
    
    #path('api/create_order/<int:pk>', create_order),
    #path('api/C_order', OrderCreateView.as_view()),
    path('api/read_order', reading_order),
    path('api/R_order', OrderListView.as_view()),
    #path('api/update_order/<int:pk>', update_order),
    #path('api/U_order/<int:id>', OrderUpdateView.as_view()),
    path('api/delete_order/<int:pk>', delete_order),
    path('api/D_order/<int:pk>', OrderDeleteView.as_view()),
    
    path('api/read_orderitem', reading_orderitem),
    path('api/R_orderitem', OrderItemListView.as_view()),
    path('api/U_orderitem/<int:pk>', OrderItemUpdateView.as_view()),
    path('api/delete_orderitem/<int:pk>', delete_orderitem),
    path('api/D_orderitem/<int:pk>', OrderItemDeleteView.as_view()),
    
    path('api/users', UserList.as_view()),
    path('api/register', RegisterAPIView.as_view()),
    path('api/login', LoginView.as_view()),
    path('api/logout', logout_view),
    path('api/request_pass',RequestPasswordReset.as_view()),
    #path('api/reset_pass',PasswordResetConfirmView.as_view()),
    
    #HTML
    path('home/' , index , name="home"),
    path('compair/', compair , name="compair"),
    path('components/', components , name="components"),
    path('contact/', contact , name="contact"),
    path('faq/', faq , name="faq"),
    path('forgetpass/' , forgetpass , name="forgetpass"),
    path('legal_notice/' , legal_notice , name="notice"),
    path('normal/' , normal , name="normal"),
    path('product_details/' , product_details , name="details"),
    path('product_summary/' , product_summary , name="summary"),
    path('products/' , products , name="products"),
    path('register/' , register , name="register"),
    path('special_offer/' , special_offer , name="offer"),
    path('tac/' , tac , name="tac"),
    path('login/', login , name="login"),
    
    path('index2/', index2),
]