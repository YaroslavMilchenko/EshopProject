from django.urls import path
from . import views
from .views import SignUpView

urlpatterns = [
    path('', views.category_list, name = 'category-list'),
    path('category/<int:category_id>/', views.product_list, name = 'product-list'),
    path('signup/', SignUpView.as_view(), name='signup')
]