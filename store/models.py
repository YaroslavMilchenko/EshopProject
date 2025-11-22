from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    # upload_to: creates subfolders by year/month (to avoid lumping everything together)
    # blank=True: allows you to create a product WITHOUT an image (to prevent old products from breaking)
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True, verbose_name='Image')
    
    def __str__(self):
        return self.name
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="User") #if user delete account, order not delete
    first_name = models.CharField(max_length=200, verbose_name="Name")
    last_name = models.CharField(max_length=200, verbose_name="Surname")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    address = models.CharField(max_length=250, verbose_name="Address")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Order date")
    paid = models.BooleanField(default=False, verbose_name="Paid")
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Order"
        verbose_name_plural= "Orders"
        
    def __str__(self):
        return f'Order {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Order")
    product = models.ForeignKey(Product, related_name='oreder_items', on_delete=models.SET_NULL, null = True, verbose_name="Product")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    
    class Meta:
        verbose_name = "Order item"
        verbose_name_plural = "Order items"
        
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity