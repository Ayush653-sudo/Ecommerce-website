from django.db import models
from .product import Product
from .customer import Customer
import datetime


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    email=models.EmailField(max_length=30,default="tomarms2@yahoo.co.in")
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    pincode = models.CharField(default=0,max_length=9)
    status = models.CharField(max_length=20,default="cash on dilevry")
    objects=models.Manager()


  
   
    @staticmethod
    def get_orders_by_customer(email_s):
        
        return Order.objects.filter(email=email_s)


    