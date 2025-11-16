from django.shortcuts import render
from .models import Category, Product
from django.views import generic
from .forms import CustomerUserCreationForm
from django.urls import path, reverse_lazy

def category_list(request):
    all_categories = Category.objects.all()
    
    context = {
        'categories': all_categories,
    }
    return render(request, 'store/category_list.html', context)

def product_list(request, category_id):
    category = Category.objects.get(id = category_id)
    products_in_category = Product.objects.filter(category=category)
    
    context = {
        'products': products_in_category,
        'category': category
    }
    
    return render(request, 'store/product_list.html', context)

class SignUpView(generic.CreateView):
    form_class = CustomerUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    