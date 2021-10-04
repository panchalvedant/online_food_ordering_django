from django.db import models
import random
# Create your models here.
from django.db import models
from OrderingOnline.models import customer
from django.contrib.auth.models import User,AbstractUser
from delivery_boy.models import deliveryboy
from django.utils import timezone
from datetime import date
# Create your models here.
import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure




    
class Account(models.Model):
    id=models.AutoField(primary_key=True)
    user_account=models.ForeignKey(customer, on_delete=models.CASCADE)
    account_no=models.CharField(max_length=12,default=None)
    bank_password=models.CharField(max_length=12,default=None)
    
    def save_otp(self):
        account_sid = AC75173bb622333cb934fbdb95b68e90ce
        auth_token = d2de390e6a58a0df1b39370a63ed0bb6
        otp=random(1000,5000)
        client = Client(account_sid, auth_token)
        message = client.messages.create(
                body='your otp is {}'.format(otp),
                from_=+12242231053,
                to='9328003668'
        )
        print(otp)
        return otp
   
        
    
    
class restaurant(models.Model):
    Restaurant_name=models.CharField(max_length=50,default=None)
    Restaurant_photo=models.ImageField(upload_to='restaurant_images/')
    status=models.BooleanField(default=False)
    password=models.CharField(default=None,max_length=30)
    uname=models.CharField(max_length=30,default=None)
    email=models.EmailField(max_length=50,default=None)
    mobile=models.CharField(max_length=10)
    address=models.CharField(max_length=150)
    state=models.CharField(max_length=20)
    city=models.CharField(max_length=20)
    feedback=models.DecimalField(max_digits=1,decimal_places=1,default=0.0)
    def __str__(self):
        return self.Restaurant_name
    
class Category(models.Model):
    id=models.IntegerField(primary_key=True)
    cname=models.CharField(max_length=20,default="Special")
    
    def __str__(self):
        return self.cname
   
class Item(models.Model):
    id=models.AutoField(primary_key=True)
    rdata=models.ManyToManyField(restaurant,related_name='rest_items')
    pname=models.CharField(max_length=50)
    pdesc=models.CharField(max_length=150,default="delicious")
    price=models.DecimalField(max_digits=10, decimal_places=6)
    pimage=models.ImageField(upload_to='menu_images/')
    category=models.CharField(max_length=150,default="delicious")
    total=models.DecimalField(max_digits=10, decimal_places=6,default=0.0)
    discount=models.DecimalField(max_digits=10, decimal_places=6,default=0)
    feedback=models.DecimalField(max_digits=10, decimal_places=6,default=0)
    
    def __str__(self):
        return self.pname
    
    
class cart(models.Model):
    id=models.AutoField(primary_key=True)
    userdata=models.ForeignKey(customer, on_delete=models.CASCADE)
    Items_data=models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    final_amount=models.DecimalField(max_digits=10, decimal_places=6,default=0)
    delivery_charge=models.DecimalField(max_digits=8,decimal_places=6,default=40.00)
    
    def return_items_id(self):
        return id
    
    def __str__(self):
        return "added"
    
class favourite(models.Model):
    id=models.AutoField(primary_key=True)
    userdata=models.ForeignKey(customer, on_delete=models.CASCADE)
    Items_data=models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    final_amount=models.DecimalField(max_digits=10, decimal_places=6,default=0)
    
    def return_items_id(self):
        return id
    
    def __str__(self):
        return "favourite add"
    
class OrderProduct(models.Model):
    id=models.AutoField(primary_key=True)
    created_on=models.DateTimeField(default=timezone.now())
    status=models.CharField(max_length=150,default="not_delivered")
    price=models.DecimalField(max_digits=10, decimal_places=6)
    userdata=models.ForeignKey(customer, on_delete=models.CASCADE)
    cartdata=models.ForeignKey(cart, on_delete=models.CASCADE)
    # Items_data=models.ForeignKey(Item, on_delete=models.CASCADE)
    # rdata=models.ManyToManyField(restaurant,related_name='rest_order')
    
    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'
    
    def update_order(self):
        self.status="delivered"  


class Order_confirm(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(customer,on_delete=models.SET_NULL,null=True)
    Item=models.ForeignKey(Item, on_delete=models.SET_NULL,null=True)
    price=models.DecimalField(max_digits=19, decimal_places=10)
    status=models.CharField(max_length=15,default="Ordered")
    feedback=models.IntegerField(default=0)
    created_on=models.DateField(default=timezone.now())
    delivery_charge=models.DecimalField(max_digits=10,decimal_places=6,default=40.00)
    delivery_boy=models.ForeignKey(deliveryboy,on_delete=models.SET_NULL,null=True)
    waiting_status=models.BooleanField(default=False)
    quantity=models.IntegerField()
    


class offer(models.Model):
    name=models.CharField(max_length=10)
    Item=models.ForeignKey(Item, on_delete=models.CASCADE)
    discount=models.DecimalField(max_digits=19, decimal_places=10,default=0)
    
    def __str__(self):
        return self.name
