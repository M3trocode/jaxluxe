from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    
    
    def __str__(self):
        return self.full_name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    digital = models.BooleanField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
            return url    
        
class Order(models.Model):
        customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
        #products = models.ManyToManyField( through='OrderItem')
        total_amount = models.DecimalField(max_digits=10, decimal_places=2)
        transaction_id = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return str(self.id)
        @property
        def get_cart_total(self):
            orderitems = self.order.orderitem_set.all()
            total =  sum([item.get_total for item in orderitems])
            return total
        @property
        def get_cart_total(self):
            orderitems = self.order.orderitem_set.all()
            total =  sum([item.quantity for item in orderitems])
            return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class Shipping(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address          
    