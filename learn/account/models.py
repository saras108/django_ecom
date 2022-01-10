from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True , on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200 , null=True)
    email = models.CharField(max_length=200 , null= True)
    profile_pic = models.ImageField(default = "profile.png" ,  null = True , blank = True)    
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    CATAGORY = (
        ('Indoor' , 'Indoor'),
        ('Outdoor' , 'Outdoor')
    )
    name = models.CharField(max_length=200, null=True)
    tag = models.ManyToManyField(Tag)
    img = models.ImageField(default = "profile.png" ,  null = True , blank = True, upload_to="products")    
    price = models.FloatField(null=True)
    catagory = models.CharField(max_length=200, null=True , choices=CATAGORY)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.name
        

class Order(models.Model):
    STATUS = (
        ('Pending' , 'Pending'),
        ('Out of delivery', 'Out of delivery'),
        ('Delivered' , 'Deliverd')
    )
    customer = models.ForeignKey(Customer , null=True  , on_delete=models.SET_NULL)
    product = models.ForeignKey(Product , null=True , on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True , null=True)
    status = models.CharField(max_length=200 , null = True , choices=STATUS)

    
    def __str__(self):
        return self.product.name
