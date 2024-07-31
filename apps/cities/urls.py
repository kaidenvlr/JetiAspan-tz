from django.urls import path
from .views import ProductAPIView, CityListAPIView, ProductImageAPIView, ProductListAPIView

urlpatterns = [
    path('products/<int:city_id>/', ProductAPIView.as_view(), name='products'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),

    path('cities/', CityListAPIView.as_view(), name='city-create'),
    path('product-images/', ProductImageAPIView.as_view(), name='product-image-create'),
]
