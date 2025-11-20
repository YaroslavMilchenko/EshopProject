from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Order, OrderItem
from django.views import generic
from .forms import CustomerUserCreationForm, OrderCreateForm
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

def decrease_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1
            messages.success(request, f'Product quantity reduced')
        else:
            del cart[product_id_str]
            messages.success(request, f'Product was remove from your cart')
    
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart-detail')
    

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

def order_create(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, f'Your cart is empty')
        return redirect('caregory-list')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
                order.save()
                products = Product.objects.filter(id__in = cart.keys())
                
                for product in products:
                    quantity = cart[str(product.id)]
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=product.price,
                        quantity = quantity,
                    )
                del request.session['cart']
                request.session.modified = True
                
                return render(request, 'store/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
        
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email
            }
            form = OrderCreateForm(initial=initial_data)
    
    cart_items = []
    total_price = 0
    products = Product.objects.filter(id__in = cart.keys())
    for product in products:
        quantity = cart[str(product.id)]
        item_total_price = quantity * product.price
        cart_items.append({
            'product':product,
            'quantity': quantity,
            'item_total_price': item_total_price,
        })
        total_price += item_total_price
        
    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'store/checkout.html', context)

@login_required
def order_history(request):
    my_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': my_orders,
    }
    return render(request, 'store/order_history.html', context)