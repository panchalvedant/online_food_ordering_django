from django.db import models

# Create your models here.


#pip install stripe for payment
# Create your models here.
class user(models.Model):
    id=models.IntegerField(primary_key=True)
    uname=models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    
    
class customer(models.Model):
    id=models.IntegerField(primary_key=True)
    uname=models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    mobile=models.CharField(max_length=10)
    password=models.CharField(max_length=20)
    address=models.CharField(max_length=150)
    state=models.CharField(max_length=20)
    city=models.CharField(max_length=20)
    
    def __str__(self):
        return self.uname
    
    
class alert(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(customer,on_delete=models.SET_NULL,null=True)
    notification=models.ForeignKey('Restaurant1.Order_confirm',on_delete=models.SET_NULL,null=True)
    
class Account_user(models.Model):
    id=models.AutoField(primary_key=True)
    user_account=models.ForeignKey(customer, on_delete=models.CASCADE)
    account_no=models.CharField(max_length=12,default=None)
    bank_password=models.CharField(max_length=12,default=None)
    
   
class Item_feedback(models.Model):
    id=models.AutoField(primary_key=True)
    Item=models.ForeignKey('Restaurant1.Item',on_delete=models.SET_NULL,null=True)
    userid=models.ForeignKey(customer,on_delete=models.SET_NULL,null=True)
    feedback=models.DecimalField(max_digits=5,decimal_places=3)
    
    
    
    
    