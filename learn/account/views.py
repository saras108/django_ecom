from django.shortcuts import render

from django.http import HttpResponse
from .models import *

# Create your views here.

def home(request):
    
    orders = Order.objects.all()
    customer = Customer.objects.all()

    total_customers = customer.count()
    
    order_count = orders.count()

    deliverd = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()

    context = {'orders': orders , 'customer': customer , 'total_consumer':total_customers, 'order_count':order_count, 'deliverd': deliverd , 'pending': pending} 


    return render(request , 'accounts/dashboard.html' , context)

def products(request):
    products = Product.objects.all()
    return render(request , 'accounts/products.html' , {'product' : products})

def customer(request):
    return HttpResponse('customer page')
