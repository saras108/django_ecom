from django.shortcuts import render, redirect

from django.http import HttpResponse

from .models import *

from .forms import OrderForm , CreateUserForm , CustomerForm
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
    form = CreateUserForm()

    if request.method== 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')    

            group = Group.objects.get(name = "customer")
            user.groups.add(group)

            Customer.objects.create(user = user , name  = username)

            messages.success(request , 'Account Successfully created for ' +username)

            return redirect('login')
    
    context = {'form' : form}
    return render(request , 'accounts/registerpage.html', context)


@unauth_user
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
@admin_only
def home(request):
    
    orders = Order.objects.all()

    customer = Customer.objects.all()

    total_customers = customer.count()
    
    order_count = orders.count()

    deliverd = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()

    context = {'orders': orders , 'customer': customer , 'total_consumer':total_customers, 'order_count':order_count, 'deliverd': deliverd , 'pending': pending} 


    return render(request , 'accounts/dashboard.html' , context)

@login_required(login_url='login')
@allowed_user(allowed_roles = ['customer'])
def userpage(request):

    orders = request.user.customer.order_set.all()

    order_count = orders.count()

    deliverd = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()

    context = {'orders': orders , 'customer': customer , 'order_count':order_count, 'deliverd': deliverd , 'pending': pending} 


    # context = {'orders': orders}
    
    return render(request , 'accounts/userpage.html' , context)


@login_required(login_url='login')
@allowed_user(allowed_roles = ['customer'])
def accountSettings(request):
    user = request.user.customer

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES , instance= user)
        if form.is_valid():
            form.save()
            
    form = CustomerForm(instance= user)
    context = { 'form' : form}
    return render(request , 'accounts/account_settings.html' , context)

    

# @allowed_user(allowed_roles = ['admin'])
def products(request):
    products = Product.objects.all()
    return render(request , 'accounts/products.html' , {'product' : products})

# @allowed_user(allowed_roles = ['admin'])
def customer(request , pk):

    customer = Customer.objects.get(id = pk)
    orders = customer.order_set.all()

    orders_count = orders.count()
    my_filter = OrderFilter(request.GET , queryset= orders) 
    orders = my_filter.qs


    context = {'customer': customer , 'orders': orders , 'orders_count' : orders_count , 'my_filter':my_filter}

    # return HttpResponse(context.cus)

    return render(request , 'accounts/customer.html' , context)


# @allowed_user(allowed_roles = ['admin'])
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request , 'accounts/order_form.html' , context)


# @allowed_user(allowed_roles = ['admin'])
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

# @allowed_user(allowed_roles = ['admin'])
def deleteOrder(request , pk):
    order = Order.objects.get(id = pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    context = {'order': order}
    return render(request , 'accounts/delete.html' , context)