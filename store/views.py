from django.shortcuts import render, redirect
from django.contrib import messages
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

def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {}) #get session cart
        product_id_str = str(product_id)
        quantity = cart.get(product_id_str, 0)  #get current quantity of the product
        cart[product_id_str] = quantity + 1
        request.session['cart'] = cart      #save cart back
        request.session.modified = True     #(Important) Tell Django that the session has been modified
        messages.success(request, f'The product has been successfully added to your cart.')
        next_page = request.POST.get('next', 'category-list')
    return redirect(next_page)      
    # (request.META.get('HTTP_REFERER') is the "previous URL")

def cart_detail(request):
    cart = request.session.get('cart', {})  #get cart from session or empty dictionary
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)   #get objects from BD by product_ids
    cart_items = []
    total_price = 0
    
    for product in products:
        quantity = cart[str(product.id)]    #get quantity from session by id in dictionary
        item_total_price = product.price * quantity   #total price for this product
        
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total_price': item_total_price,
        })
        
        total_price += item_total_price
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    
    return render(request, 'store/cart_detail.html', context)
        
        