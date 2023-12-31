from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('welcome/', views.welcome, name="welcome"),
    path('cart/', views.cart, name="cart"),
    path('check/', views.check,name="check"),
    path('product/<int:product_id>/', views.product,name="product"),
    path('checkout/', views.checkout, name="checkout"),
    path('login/', views.my_login_view, name='login'),
    path('signup/', views.signup, name="signup"),
    path('categories/<str:tool>', views.categories, name="categories"),
    path('categories2/<str:tool>', views.categories2, name="categories2"),
    path('profile/', views.profile, name="profile"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
]
