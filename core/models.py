from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
import uuid
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    
    def __str__(self):
        return self.full_name
@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance, full_name=instance.username, email=instance.email)
    


class Category(models.Model):
    name = models.CharField(max_length=100,)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    digital = models.BooleanField()
    image = models.ImageField(null=True, blank=True)
    in_cart = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class CartItem(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET, null=True)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def save(self, *args, **kwargs):
        # Override save method to update total_price before saving
        self.update_total_price()
        super().save(*args, **kwargs)

        # Send email notification
        send_mail(
            'New Order Notification',
            'A new order has been made.',
            'temiloluwaogunniyi@gmail.com',  # Sender's email
            ['creativemonsterr@gmail.com'],  # Recipient's email
            fail_silently=False,
        )

        # Add your additional notification logic here if needed
        print('A new order item has been added:', self.id)

    def update_total_price(self):
        # Calculate the total price for the item based on the product price and quantity
        self.total_price = self.product.price * self.quantity

    @property
    def get_total(self):
        total = self.total_price
        return total

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Shipping(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    emailadd = models.EmailField()
    phone = models.CharField(max_length=20)
    streetadd = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    selected_state = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.firstname} {self.lastname} - Order ID: {self.id}"

class Order(models.Model):
    order_id = models.CharField(max_length=36, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shipping_info = models.ForeignKey(Shipping, on_delete=models.SET_NULL, null=True, blank=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(Product, through=OrderItem)

    def update_total_amount(self):
        # Calculate the total amount based on items in the order
        items = self.items.all()
        total_amount = sum(item.product.price * item.quantity for item in items)
        self.total_amount = total_amount
        self.save()

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        order_items = self.order_items.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_quantity(self):
        order_items = self.order_items.all()
        quantity = sum([item.quantity for item in order_items])
        return quantity

    def save(self, *args, **kwargs):
        # Save the order
        super().save(*args, **kwargs)

        # Send email notification
        send_mail(
            'New Order Notification',
            'A new order has been made.',
            'temiloluwaogunniyi@gmail.com',  # Sender's email
            ['creativemonsterr@gmail.com'],  # Recipient's email
            fail_silently=False,
        )

        # Add your additional notification logic here if needed
        print('A new order has been made:', self.id)


def generate_order_id():
    # Generate a unique order_id using the uuid module
    return str(uuid.uuid4())



