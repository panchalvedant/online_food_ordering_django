from django.db import models


# Create your models here.
class deliveryboy(models.Model):
    id=models.IntegerField(primary_key=True)
    deliveryboy_name=models.CharField(max_length=50)
    status=models.CharField(max_length=50,default="Available")
    email=models.CharField(max_length=50)
    mobile=models.CharField(max_length=10)
    password=models.CharField(max_length=20)
    address=models.CharField(max_length=150)
    state=models.CharField(max_length=20)
    city=models.CharField(max_length=20)
    salary=models.IntegerField(default=10000)
    
    def __str__(self):
        return self.deliveryboy_name
    

    