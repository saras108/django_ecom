from django.shortcuts import render, redirect

from django.http import HttpResponse
from .models import *

from .forms import OrderForm

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

def customer(request , pk):
    customer = Customer.objects.get(id = pk)
    orders = customer.order_set.all()
    orders_count = orders.count()


    context = {'customer': customer , 'orders': orders , 'orders_count' : orders_count}
    return render(request , 'accounts/customer.html' , context)


def createOrder(request):
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if(form.is_valid()):
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request , 'accounts/order_form.html' , context)


def updateOrder(request , pk):

    order = Order.objects.get(id = pk)
    form = OrderForm(instance= order)

    if request.method == 'POST':
        form = OrderForm(request.POST , instance=order)

        if(form.is_valid()):
            form.save()
            return redirect('/')
    
    context = {'form': form}
    return render(request , 'accounts/order_form.html' , context)

def deleteOrder(request , pk):
    order = Order.objects.get(id = pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    context = {'order': order}


    return render(request , 'accounts/delete.html' , context)