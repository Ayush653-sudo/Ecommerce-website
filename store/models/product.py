from django.db import models
from .category import Category
class Product(models.Model):
    name=models.CharField(max_length=50)
    price=models.IntegerField()
    gategory=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    description=models.ImageField(upload_to='uploads/products/',null=True,blank=True)
    @staticmethod
    def get_all_products():
        return Product.objects.all()
    @staticmethod
    def get_all_products_by_gategory_id(gategoryid):
        if gategoryid:
            return Product.objects.filter(gategory=gategoryid)
        else:
            return Product.get_all_products()

    @staticmethod
    def get_product_by_id(ids):

        return Product.objects.filter(id__in=ids)