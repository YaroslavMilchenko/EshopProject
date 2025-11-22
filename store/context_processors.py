def get_cart_count(request):
# Get the cart from the session (or an empty dictionary)
    cart = request.session.get('cart', {})

# Calculate the total quantity.
# cart.values() will return a list of quantities (e.g., [2, 1, 5])
    count = sum(cart.values())

# Return the dictionary.
# The 'cart_count' key will be available in ALL site templates.
    return {'cart_count': count}