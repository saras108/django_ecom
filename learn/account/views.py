from django.contrib.messages.api import success
from django.forms.forms import Form
from django.shortcuts import render, redirect

from django.http import HttpResponse

from .models import *

from .forms import OrderForm , CreateUserForm , CustomerForm , ProductForm
from .filters import OrderFilter
from .decorators import unauth_user, allowed_user , admin_only

from django.contrib import messages

from django.contrib.auth import authenticate , login , logout

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group
# from django.contrib.auth.forms import UserCreationForm

# Create your views here.

@unauth_user
def registerpage(request):
    try:        
        form = CreateUserForm()
        if request.method== 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')    
                
                #signals will do the remaning jobs.

                messages.success(request , 'Account Successfully created for ' +username)

                return redirect('login')
        
        context = {'form' : form}
        return render(request , 'accounts/registerpage.html', context)
    except:
        print("An exception occurred")

@unauth_user
def loginpage(request):
    try:
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
    except:
        return HttpResponse('ERROR OCCURED')

def logoutUser(request):
    try:
        logout(request)
        return redirect('login')
    except:
        return HttpResponse('ERROR OCCURED')


@login_required(login_url='login')
@admin_only
def home(request):
    try:  
        products = Product.objects.all()
        customer = Customer.objects.all()
        total_customers = customer.count()
        order_count = Order.objects.count()
        deliverd = Order.objects.filter(status = 'Delivered').count()
        pending = Order.objects.filter(status = 'Pending').count()
        context = {'products': products , 'customer': customer , 'total_consumer':total_customers, 'order_count':order_count, 'deliverd': deliverd , 'pending': pending} 
        return render(request , 'accounts/dashboard.html' , context)
    except:
        return HttpResponse('ERROR OCCURED')

@login_required(login_url='login')
@allowed_user(allowed_roles = ['customer', 'admin'])
def userpage(request): 
    try:   
        products = Product.objects.all()
        context = {'products': products}
        return render(request , 'accounts/userpage.html' , context)
    except:
        return HttpResponse('ERROR OCCURED')

@login_required(login_url='login')
@allowed_user(allowed_roles = ['customer'])
def cust_order(request):
    try:
        if request.method == 'POST':
            form = OrderForm(request.POST)
            form.save()
            return redirect('/')
        return HttpResponse('ERROR OCCURED')
    except:
        return HttpResponse('ERROR OCCURED')


@login_required(login_url='login')
@allowed_user(allowed_roles = ['customer'])
def myorders(request):
    try:
        orders = request.user.customer.order_set.all()
        order_count = orders.count()
        deliverd = orders.filter(status = 'Delivered').count()
        pending = orders.filter(status = 'Pending').count()
        context = {'orders': orders , 'customer': customer , 'order_count':order_count, 'deliverd': deliverd , 'pending': pending} 
        return render(request , 'accounts/myorders.html' , context)
    except:
        return HttpResponse('ERROR OCCURED')


@login_required(login_url='login')
@allowed_user(allowed_roles = ['customer'])
def accountSettings(request):
    try:
        user = request.user.customer
        if request.method == 'POST':
            form = CustomerForm(request.POST, request.FILES , instance= user)
            if form.is_valid():
                form.save()
        form = CustomerForm(instance= user)
        context = { 'form' : form}
        return render(request , 'accounts/account_settings.html' , context)
    except:
        return HttpResponse('ERROR OCCURED')


@login_required(login_url='login')
@allowed_user(allowed_roles = ['admin'])
def all_orders(request):
    try:
        orders = Order.objects.filter(status = 'Pending')
        return render(request , 'accounts/ordered_products.html' , {'orders' : orders})
    except:
        return HttpResponse('ERROR OCCURED')


@login_required(login_url='login')
@allowed_user(allowed_roles = ['admin'])
def products(request):
    try:
        products = Product.objects.all()
        return render(request , 'accounts/products.html' , {'product' : products})
    except:
        return HttpResponse('ERROR OCCURED')


@login_required(login_url='login')
@allowed_user(allowed_roles = ['admin'])
def customer(request , pk):
    try:
        customer = Customer.objects.get(id = pk)
        orders = customer.order_set.all()
        orders_count = orders.count()
        my_filter = OrderFilter(request.GET , queryset= orders) 
        orders = my_filter.qs
        context = {'customer': customer , 'orders': orders , 'orders_count' : orders_count , 'my_filter':my_filter}
        return render(request , 'accounts/customer.html' , context)
    except:
        return HttpResponse('ERROR OCCURED')


@login_required(login_url='login')
@allowed_user(allowed_roles = ['admin'])
def createOrder(request):
    try:
        form = OrderForm()
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('/')
        context = {'form': form}
        return render(request , 'accounts/order_form.html' , context)
    except:
        return HttpResponse('ERROR OCCURED')


@login_required(login_url='login')
@allowed_user(allowed_roles = ['admin'])
def updateOrder(request , pk):
    try:
        order = Order.objects.get(id = pk)
        form = OrderForm(instance= order)
        if request.method == 'POST':
            form = OrderForm(request.POST , instance=order)
            if(form.is_valid()):
                form.save()
                return redirect('/')
        
        context = {'form': form}
        return render(request , 'accounts/order_form.html' , context)
        
    except:
        return HttpResponse('ERROR OCCURED')

@login_required(login_url='login')
@allowed_user(allowed_roles = ['customer'])
def deleteOrder(request , pk):
    try:
        order = Order.objects.get(id = pk)

        if request.method == 'POST':
            order.delete()
            return redirect('/')
        
        context = {'order': order}
        return render(request , 'accounts/delete.html' , context)
    except:
        return HttpResponse('ERROR OCCURED')


@login_required(login_url='login')
@allowed_user(allowed_roles = ['admin'])
def createProduct(request):
    try:
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('/')
        form = ProductForm()
        context = {'form': form}
        return render(request , 'accounts/product_form.html' , context)
    except:
        return HttpResponse('ERROR OCCURED')
   

@login_required(login_url='login')
@allowed_user(allowed_roles = ['admin'])
def updateProduct(request , pk):
    try:
        product = Product.objects.get(id = pk)
        form = ProductForm(instance= product)
        if request.method == 'POST':
            form = ProductForm(request.POST , instance=product)
            if(form.is_valid()):
                form.save()
                return redirect('/')
        context = {'form': form}
        return render(request , 'accounts/product_form.html' , context)
    except:
        return HttpResponse('ERROR OCCURED')


@login_required(login_url='login')
@allowed_user(allowed_roles = ['admin'])
def deleteProduct(request , pk):
    try:
        product = Product.objects.get(id = pk)
        if request.method == 'POST':
            product.delete()
            return redirect('/')
        context = {'product': product}
        return render(request , 'accounts/delete_product.html' , context)
    except:
        return HttpResponse('ERROR OCCURED')