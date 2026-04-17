from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListCreateView.as_view(), name='api_products'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='api_product_detail'),
]
