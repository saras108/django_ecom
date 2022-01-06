
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('register/', views.registerpage , name = 'register'),
    path('login/', views.loginpage , name = 'login'),
    path('logout/', views.logoutUser , name = 'logout'),

    path('', views.home , name = 'home'),
    
    path('product/', views.products , name='product'),
    path('all_orders/', views.all_orders , name='all_orders'),
    path('user/', views.userpage , name='user_page'),
    path('myorders/', views.myorders , name='myorders'),
    path('account/', views.accountSettings , name='account'),
    path('customer/<str:pk>/', views.customer , name='consumer'),

    path('create_order_user/', views.cust_order , name='create_order_user'),
    path('create_order/', views.createOrder , name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder , name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder , name='delete_order'),


    path('create_product/', views.createProduct , name='create_product'),
    path('update_product/<str:pk>/', views.updateProduct , name='update_product'),
    path('delete_product/<str:pk>/', views.deleteProduct , name='delete_product'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = "accounts/password_reset.html"),
        name='reset_password'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = "accounts/password_reset_sent.html"),
        name='password_reset_done'),

    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "accounts/password_reset_form.html"),
         name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name = "accounts/password_reset_done.html") ,
        name='password_reset_complete'),

]