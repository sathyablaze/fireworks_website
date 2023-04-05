from django.db import models
from django.contrib.auth.models import User
import math

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__ (self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.IntegerField()
    image = models.ImageField(null=True, blank=True)

    def __str__ (self):
        return self.name    
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null = True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100,null=True)

    def __str__ (self):
        return str(self.id)
    
    @property
    def get_cart_subtotal(self):
        orderitems = self.orderitem_set.all()
        subtotal = sum([item.get_total for item in orderitems])
        return subtotal
    
    @property
    def get_cart_gst(self):
        orderitems = self.orderitem_set.all()
        subtotal = sum([item.get_total for item in orderitems])
        gst = math.ceil(18/100 * subtotal)
        return gst
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        subtotal = sum([item.get_total for item in orderitems])
        gst = math.ceil(18/100 * subtotal)
        total = gst + subtotal
        return total
    
    # @property
    # def get_cart_quantity(self):
    #     orderitems = self.orderitem_set.all()
    #     quantity = sum(item.quantity for item in orderitems)
    #     return quantity
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=20, null=True)
    date_added = models.DateField(auto_now_add=True)

    
    def __str__ (self):
        return self.address



