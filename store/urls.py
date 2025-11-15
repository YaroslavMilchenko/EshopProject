from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name = 'category-list'),
    path('category/<int:category_id>/', views.product_list, name = 'product-list')
]