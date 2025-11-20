from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Order

class CustomerUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
        
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order  
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        labels = {
            'first_name': 'Your name',
            'last_name': 'Your surname',
            'email': 'Email',
            'phone': 'Phone',
            'address': 'Address'
        }