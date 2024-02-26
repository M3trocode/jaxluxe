from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order, Shipping
from django import forms




class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        
class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Your password must contain at least one number, one lowercase and one uppercase letter, and at least 8 or more characters."
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        # Your custom password validation logic goes here
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("Password must contain at least one number.")
        if not any(char.islower() for char in password1):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password1
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ['firstname', 'lastname', 'emailadd', 'phone', 'streetadd', 'town', 'zip_code', 'selected_state']