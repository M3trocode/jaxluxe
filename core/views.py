from django.shortcuts import render
from .models import *

# Create your views here.

def index(request):
    context ={}
    return render(request, 'core/index.html',context)

def welcome(request):
    context ={}
    return render(request, 'core/welcome.html',context)

def product(request):
    products = Product.objects.all
    context = {'products':products}
    return render(request, 'core/product.html',context)

def check(request):
    context ={}
    return render(request, 'core/check.html',context)

def checkout(request):
    context ={}
    return render(request, 'core/checkout.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()  # Assuming 'orderitem' is the related name in your Order model

        context = {'items': items}
    else:
        context = {'items': []}

    return render(request, 'core/cart.html', context)



def categories(request):
    products = Product.objects.all
    context = {'products':products}
    return render(request, 'core/categories.html',context)

def categories2(request):
    context ={}
    return render(request, 'core/categories2.html',context)

def login(request):
    context ={}
    return render(request, 'core/login.html',context)

def signup(request):
    context ={}
    return render(request, 'core/signup.html',context)