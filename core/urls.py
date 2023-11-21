from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('welcome.html/', views.welcome, name="welcome"),
    path('cart.html/', views.cart, name="cart"),
    path('check.html/', views.check,name="check"),
    path('product.html/', views.product,name="product"),
    path('checkout.html/', views.checkout, name="checkout"),
    path('login.html/', views.login, name="login"),
    path('signup.html/', views.signup, name="signup"),
    path('categories.html/', views.categories, name="categories"),
    path('categories2.html/', views.categories2, name="categoroies2"),
    
]
