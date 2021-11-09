from django.db import models


class Customer(models.Model):
    first_name=models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone=models.CharField(max_length=13,unique=True)
    email=models.EmailField(max_length=30,unique=True)
    password = models.CharField(max_length=25)

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

