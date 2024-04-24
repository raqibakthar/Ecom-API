from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):

    product_id = models.AutoField(primary_key=True,editable=False)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=55,null=True,blank=True)
    image = models.ImageField(null=True,blank=True,default='/sample_image.jpg')
    brand = models.CharField(max_length=55,null=True,blank=True)
    category = models.CharField(max_length=255,null=True,blank=True)
    description =models.TextField( null=True,blank=True)
    rating =models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    numReviews = models.IntegerField(null=True,blank=True)
    price = models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    countInStock = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class Review(models.Model):

    review_id = models.AutoField(primary_key=True,editable=False)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=55,null=True,blank=True)
    rating = models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    comment = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name
    
class Order(models.Model):

    order_id = models.AutoField(primary_key=True,editable=False)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    payment_method = models.CharField(max_length=255,null=True,blank=True)
    tax_price = models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    shipping_price = models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    total_price = models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add = True)
    delivered_at = models.DateTimeField(auto_now_add = True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.created_at)
    
class OrderItems(models.Model):

    order_item_id = models.AutoField(primary_key=True,editable=False)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=55,null=True,blank=True)
    qty = models.IntegerField(null=True,blank=True,default=0)
    price = models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    image = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self) -> str:
        return str(self.name)
    
class ShippingAddress(models.Model):

    shipping_add_id = models.AutoField(primary_key=True,editable=False)
    order = models.OneToOneField(Order,on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255,null=True,blank=True)
    postal_code = models.CharField(max_length=255,null=True,blank=True)
    country = models.CharField(max_length=255,null=True,blank=True)
    shipping_price = models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)

    def __str__(self) -> str:
        return str(self.name)