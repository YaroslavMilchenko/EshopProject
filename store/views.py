from django.shortcuts import render
from .models import Category, Product

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