from django.contrib import admin
from .models import Category, Product, Order, OrderItem

admin.site.register(Category)
admin.site.register(Product)

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'created_at']
    list_filter = ['created_at']
    inlines = [OrderItemInLine]