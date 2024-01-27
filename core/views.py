import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import OrderForm, CreateUserForm, CheckoutForm
from decimal import Decimal
import json
from .forms import CheckoutForm

def index(request):
    context = {}
    return render(request, 'core/index.html', context)

def welcome(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'core/welcome.html', context)

def aboutus(request):
    context = {}
    return render(request, 'core/aboutus.html', context)

def dashboard(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'core/dashboard.html', context)

def product(request, product_id):
    # Fetch the specific product using the product_id
    product = get_object_or_404(Product, id=product_id)

    # You can add more context variables if needed
    context = {'product': product}

    return render(request, 'core/product.html', context)

def check(request):
    context = {}
    return render(request, 'core/check.html', context)

def checkout(request):
    context = {}
    return render(request, 'core/checkout.html', context)

def profile(request):
    context = {}
    return render(request, 'core/profile.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order_items = OrderItem.objects.filter(order__customer=customer)


        context = {'order_items': order_items}
        return render(request, 'core/cart.html', context)
    else:
        # Handle the case where the user is not authenticated
        context = {'order_items': []}
        return render(request, 'core/cart.html', context)


@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        # Extract data from the AJAX request
        quantity = int(request.POST.get('quantity', 1))
        product_name = request.POST.get('product_name', '')
        product_price = Decimal(request.POST.get('product_price', 0))

        # Find the product based on its name (you might want to use a unique identifier)
        product = get_object_or_404(Product, name=product_name)

        # Check if there is an existing order for the user; create one if not
        order, created = Order.objects.get_or_create(customer=request.user.customer, is_ordered=False)

        # Check if the product is already in the order; create one if not
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

        # Update the quantity and total price
        order_item.quantity = quantity
        order_item.update_total_price()
        order_item.save()

        # Update the total amount for the order
        order.update_total_amount()

        # Redirect to the cart page
        return JsonResponse({'product_id': order_item.product.id})

    return JsonResponse({'error': 'Invalid request.'})

from django.shortcuts import render



def categories(request, tool):
    tool = tool.replace('-', ' ')
    try:
        category = Category.objects.get(name=tool)
        products = Product.objects.filter(category=category)
        context = {'products': products, 'category': category}
        return render(request, 'core/categories.html', context)
    except Category.DoesNotExist:
        messages.success(request, "That Category Doesn't exist")
        return redirect('categories2')

def categories2(request, tool):
    tool = tool.replace('-', ' ')
    try:
        category = Category.objects.get(name=tool)
        products = Product.objects.filter(category=category)
        context = {'products': products, 'category': category}
        return render(request, 'core/categories2.html', context)
    except Category.DoesNotExist:
        messages.success(request, "That Category Doesn't exist")
        return redirect('home')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def my_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('welcome')

    context = {}
    return render(request, 'core/login.html', context)

def signup(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'core/signup.html', context)

def orderapproved(request):
    context = {}
    return render(request, 'core/orderapproved.html', context)

@csrf_exempt
def checkout_post(request):
    if request.method == 'POST':
        print("REQUEST: ", request)
        data = json.loads(request.body.decode('utf-8'))
        customer = request.user.customer
        print("DATA: ", data)
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        emailadd = data.get('emailadd')
        phone = data.get('phone')
        streetadd = data.get('streetadd')
        town = data.get('town')
        zip_code = data.get('zip')
        selected_state = data.get('selectedState')
        shipping_fee = data.get('shippingFee')
        orderItems = data.get('orderItems')

        def generate_order_id(): 
            prefix = "JL-" 
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7)) 
            order_id = prefix + random_suffix 
            return order_id
            
        
        shipping = Shipping(
            firstname=firstname,
            lastname=lastname,
            emailadd=emailadd,
            phone=phone,
            streetadd=streetadd,
            town=town,
            zip_code=zip_code,
            selected_state=selected_state
        )
        shipping.save()
        order_id = generate_order_id()
        order=Order(customer=customer, shipping_info=shipping, order_id=order_id)
        
        order.save()
        
        totalfee = shipping_fee
        email_text = f'You have a new order. Order ID: {order_id}'
        
        email_text += f"\nNAME:{firstname} {lastname}\nPHONE:{phone}\nEMAIL:{emailadd}\n ADDRESS:{streetadd}, ({town} {selected_state}, NIGERIA)" 
        
        for i in range(len(orderItems)):
            item = orderItems[i]
            product_id = item.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            if not product:
                return JsonResponse({'success': False, 'error': f"product {product_id} doesn't exist"})
            quantity = int(item.get('quantity'))
            if quantity > product.quantity:
                return JsonResponse({'success': False, 'error': f"not enough stock for {product.name}"})
            price = quantity * product.price 
            order_item = OrderItem(
                order=order,
                product=product,
                total_price=price,
                quantity=quantity
            )
            order_item.save()
            product.quantity = product.quantity - quantity
            product.save()
            totalfee += price
            email_text += f"\n {i + 1}. {product.name} {product.price} x {quantity} = NGN{price}\n"
        email_text += f"\n TOTAL: NGN{totalfee}\n"
        
        send_mail(
            'New Order',
            email_text,
            'temiloluwaogunniyi@gmail.com',
            ['abikeomolademakinde@gmail.com'],
            fail_silently=False,
        )

        
        context = {
            'order_id': order_id, 'totalfee': totalfee,
            
        }

        return JsonResponse({'success': True, 'data': context})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


