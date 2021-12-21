from re import U
from django.shortcuts import render, redirect

# from django.http import HttpResponse

from .models import *

from .forms import OrderForm , CreateUserForm
from .filters import OrderFilter

from django.contrib import messages

from django.contrib.auth import authenticate , login , logout

from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def registerpage(request):
    form = CreateUserForm()

    if request.method== 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')    
            messages.success(request , 'Account Successfully created for ' +user)

            return redirect('login')
    
    context = {'form' : form}
    return render(request , 'accounts/registerpage.html', context)

def loginpage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request , username = username , password = password)

        if user is not None:
            login( request , user)
            return redirect('home')
        else:
            messages.info(request , 'Invalid Username or Password')

        # return 'jmfnsd'
    context = {}
    return render(request , 'accounts/loginpage.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
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


    my_filter = OrderFilter(request.GET , queryset= orders) 

    orders = my_filter.qs


    context = {'customer': customer , 'orders': orders , 'orders_count' : orders_count , 'my_filter':my_filter}
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