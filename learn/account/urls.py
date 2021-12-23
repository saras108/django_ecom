
from django.urls import path
from . import views


urlpatterns = [

    path('register/', views.registerpage , name = 'register'),
    path('login/', views.loginpage , name = 'login'),
    path('logout/', views.logoutUser , name = 'logout'),

    path('', views.home , name = 'home'),
    
    path('product/', views.products , name='product'),
    path('user/', views.userpage , name='user_page'),
    path('customer/<str:pk>/', views.customer , name='consumer'),

    path('create_order/', views.createOrder , name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder , name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder , name='delete_order'),
]